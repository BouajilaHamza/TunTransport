import streamlit as st
from pymongo import MongoClient
import requests 
import json
import pandas as pd

client = MongoClient('mongodb://localhost:27017/')
db = client['Transport']
collection = db["soretras"]
tarif_soretras = db["tarif_soretras"]
tarif_srtm = db["tarif_srtm"]
departs =list(collection.find({},{"_id":0}))
departs = [list(depart.keys())[0] for depart in departs]
depart = st.selectbox(
    "Select your departure station :",
    list(departs))
st.write("You selected:", depart)
destination = st.selectbox(
    "Select your destination station :",
    list(departs))
st.write("You selected:", destination)

if st.button("Get Soretras data"):

    url = "http://localhost:6800/schedule.json"
    data_soretras = {
        'project': 'default',
        'spider': 'soretras',
        "depart":depart,
        "destination":destination
    }
    data_srtm = {
        'project': 'default',
        'spider': 'srtm',
        "depart":depart,
        "destination":destination
    }
    requests.post(url, data=data_soretras)
    requests.post(url, data=data_srtm)
soretras = pd.DataFrame(list(tarif_soretras.find({},{"_id":0})))
srtm = pd.DataFrame(tarif_srtm.find({},{"_id":0}))
df = pd.concat([soretras,srtm],axis=0)
st.write(df)
tarif_srtm.delete_many({})
tarif_soretras.delete_many({})

    
        
