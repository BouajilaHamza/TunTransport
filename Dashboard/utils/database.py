import json
import os

import redis
import streamlit as st
from pymongo import MongoClient
from utils.ETL import clean_filter
from utils.scraping import get_available_destinations

# Connect to Redis using environment variables
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
mongo_uri = os.getenv("MONGO_URI")


# @st.cache_resource(show_spinner=False)
def init_mongo():
    client = MongoClient(mongo_uri)
    db = client["Transport"]
    collection = db["Places"]
    dests = db["Destinations"]
    tarif_collecion = db["Tarif"]
    return collection, dests, tarif_collecion


def get_dests_from_mongo(collection, selected_departure: str, selected_companies: list):
    filter = (
        {"Depart": selected_departure["Name"], "Company": {"$in": selected_companies}}
        if selected_companies
        else {"Depart": selected_departure}
    )
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


r = redis.Redis(host=redis_host, port=redis_port, db=0)


# Example function to get data with caching logic
def get_data(query, collection, selected_departure: str, selected_companies: list):
    # Check if data is cached in Redis
    cached_data = r.get(query)
    if cached_data:
        return json.loads(cached_data)  # Return cached data

    # If not cached, fetch from MongoDB (implement this function)
    data = get_dests_from_mongo(collection, selected_departure, selected_companies)

    # Cache the result in Redis for future requests (set expiration time if needed)
    r.set(query, json.dumps(data), ex=3600)  # Cache for 1 hour

    return data
