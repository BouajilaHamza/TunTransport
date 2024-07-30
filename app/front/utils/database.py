from pymongo import MongoClient
import streamlit as st
from utils.ETL import clean_filter
from utils.scraping import get_available_destinations


@st.cache_resource(show_spinner=False)
def init_mongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Transport']
    collection = db["Places"]
    dests = db["Destinations"]
    return collection, dests





def get_dests_from_mongo(collection,selected_departure:str, selected_companies:list):
    filter = {"Depart":selected_departure["Name"],"Company": {"$in": selected_companies}} if selected_companies else {"Depart":selected_departure}
    raw_dests,clean_dests = clean_filter(collection,filter)
    if len(clean_dests) == 0:
        with st.spinner("Getting data from the web ..."):
            get_available_destinations(selected_departure["Name"], selected_departure["Id"], selected_departure["Company"])
            raw_dests,clean_dests = clean_filter(collection,filter)
    return raw_dests,clean_dests
