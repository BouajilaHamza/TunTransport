import json
import os

import redis
import streamlit as st
from pymongo import MongoClient
from redis.commands.json.path import Path
from redis.commands.search.field import NumericField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from utils.ETL import clean_filter
from utils.scraping import get_available_destinations

# Connect to Redis using environment variables
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
mongo_uri = os.getenv("MONGO_URI")

r = redis.Redis(host=redis_host, port=redis_port, db=0)
schema = (
    TextField("$.Depart", as_name="depart"),
    NumericField("$.Id", as_name="id"),
    TextField("$.Name", as_name="name"),
    TextField("$.Company", as_name="company"),
)
r.ft().dropindex()
r.ft().create_index(
    schema,
    definition=IndexDefinition(prefix=["destination:"], index_type=IndexType.JSON),
)


# @st.cache_resource(show_spinner=False)
def init_mongo():
    client = MongoClient(mongo_uri)
    db = client["Transport"]
    collection = db["Places"]
    dests = db["Destinations"]
    tarif_collecion = db["Tarif"]
    return collection, dests, tarif_collecion


def get_dests_from_mongo(collection, selected_departure: str, filter: dict):
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


# Example function to get data with caching logic
def get_data(query, collection, selected_departure, filter):
    # Check if data is cached in Redis
    cached_data = r.get(query)
    if cached_data:
        return json.loads(cached_data)  # Return cached data
    # If not cached, fetch from MongoDB (implement this function)
    data = get_dests_from_mongo(collection, selected_departure, filter)

    # Cache the result in Redis for future requests (set expiration time if needed)
    r.json().set("destination:1", Path.root_path(), data)  # Cache for 1 hour
    cursor = 0
    while True:
        cursor, keys = r.scan(cursor)
        for key in keys:
            st.write(key)
        if cursor == 0:
            break
    return data
