import json
import os

import redis
import streamlit as st
from pymongo import MongoClient
from redis.commands.json.path import Path
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from utils.ETL import clean_filter
from utils.scraping import get_available_destinations

# Connect to Redis using environment variables
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
mongo_uri = os.getenv("MONGO_URI")

r = redis.Redis(host=redis_host, port=redis_port, db=0)
schema = (
    TextField("$.Name", as_name="name"),
    TextField("$.Id", as_name="id"),
    TextField("$.Company", as_name="company"),
    TextField("$.Depart", as_name="depart"),
)

try:
    r.ft("destinations_index").create_index(
        schema,
        definition=IndexDefinition(prefix=["destination:"], index_type=IndexType.JSON),
    )
except Exception as e:
    print(f"Index creation error: {e}")


def init_mongo():
    client = MongoClient(mongo_uri)
    db = client["Transport"]
    departs_collection = db["Departs"]
    destination_collection = db["Destinations"]
    tarif_collecion = db["Tarif"]
    return departs_collection, destination_collection, tarif_collecion


def get_dests_from_mongo(collection, selected_departure: dict, filter: dict):
    raw_dests, clean_dests = clean_filter(collection, filter)
    if len(clean_dests) == 0:
        with st.spinner("Getting data from the web ..."):
            get_available_destinations(
                selected_departure["Name"],
                selected_departure["Id"],
                selected_departure["Company"],
            )
            raw_dests, clean_dests = clean_filter(collection, filter)
    return raw_dests, clean_dests


def get_dests_from_redis(company=None, name=None, id=None, depart=None):
    # Start building the query
    filters = []

    # Add filters based on provided parameters
    if company:
        # If multiple companies are provided, split them and join with '|'
        if isinstance(company, list):
            company_filter = "|".join([f"@company:{c}" for c in company])
            filters.append(f"({company_filter})")
        else:
            filters.append(f"@company:{company}")

    if depart:
        filters.append(f"@depart:{depart}")

    if name:
        filters.append(f"@name:{name}")

    if id:
        filters.append(f"@id:{id}")

    # Combine filters with AND logic
    if filters:
        query_string = " AND ".join(filters)
    else:
        query_string = "*"  # No filters, match everything
    query = Query(query_string).paging(0, 5)
    result = r.ft("destinations_index").search(query)

    return result.docs  # ,result.total


def get_data(collection, selected_departure: dict, filter: dict):
    company = filter["Company"]["$in"]
    depart = filter["Depart"]
    raw_dests = get_dests_from_redis(company=company, depart=depart)
    if raw_dests:
        # st.write(f"fetching data from redis : {filter}")
        clean_dests = [json.loads(doc["json"])["Name"] for doc in raw_dests]
        raw_dests = [json.loads(doc["json"]) for doc in raw_dests]

        return raw_dests, clean_dests
    # If not cached, fetch from MongoDB (implement this function)
    st.write(f"Fetching data from MongoDB for query '{filter}'")
    raw_dests, clean_dests = get_dests_from_mongo(
        collection, selected_departure, filter
    )

    # Cache the result in Redis for future requests (set expiration time if needed)
    for dest in raw_dests:
        document_id = f"destination:{str(dest['_id'])}"
        dest.pop("_id")
        try:
            dest["Id"] = str(dest["Id"])
        except TypeError:
            pass
        r.json().set(document_id, Path.root_path(), dest)
    return raw_dests, clean_dests
