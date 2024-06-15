import streamlit as st
from pymongo import MongoClient
import requests 
import json
import pandas as pd

client = MongoClient('mongodb://localhost:27017/')
db = client['Transport']
collection = db["soretras"]
tarif_collection = db["tarif"]
departs =list(collection.find({},{"_id":0}))
departs = [list(depart.keys())[0] for depart in departs]
depart = st.selectbox(
    "Select your departure station :",
    list(departs))
st.write("You selected:", depart)
destination = st.selectbox(
    "Select your destination station :",
    list(departs))
st.write("You selected:", depart)

if st.button("Get Soretras data"):

    url = "http://localhost:6800/schedule.json"
    data = {
        'project': 'default',
        'spider': 'soretras',
        "depart":depart,
        "destination":destination
    }
    requests.post(url, data=data)
    tarif = pd.DataFrame(list(tarif_collection.find({},{"_id":0})))
    st.write(tarif)
    # tarif_collection.drop()
    
        
