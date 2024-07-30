import time
import streamlit as st
from pymongo import MongoClient
import requests 
import json
import pandas as pd

client = MongoClient('mongodb://localhost:27017/')
db = client['Transport']
collection = db["Places"]
dests = db["Destinations"]
# Streamlit UI
st.title("Transport Booking System")
selected_companies = st.multiselect("Select Departure Time", ["SRTM", "SRTG", "Soretras"])
filter = {"Company": {"$in": selected_companies}} if selected_companies else {}
raw_data = list(collection.find(filter))
data = [i["Name"] for i in raw_data]
if len(data) == 0:
    with st.spinner("Getting data from the web ..."):
        url = "http://localhost:6800/schedule.json"
        payload = {
            'project': 'default',
            'spider': 'dests',
        }
        response = requests.post(url, data=payload)
        time.sleep(15)
    
# Select box for departures
selected_departure = st.selectbox("Select Departure Time", data)
# Conditional select box for destinations
if selected_departure:
    with st.spinner("Loading Destinations ..."):
        dests.drop()
        selected_dict = [i for i in raw_data if i["Name"]==selected_departure][0]

        url = "http://localhost:6800/schedule.json"
        payload = {
            'project': 'default',
            'spider': 'deps',
            "depart":selected_departure,
            "dep_id":selected_dict["Id"],
            "Company":selected_dict["Company"]
        }
        response = requests.post(url, data=payload)
        time.sleep(10)
    dests =list(dests.find({},{"_id":0}))
    dests = [i["Name"] for i in dests]
    # dests = dests[dests["Company"]==company]
    # dests = dests["Name"].unique()
    # dests = list(dests)
    selected_destination = st.selectbox(f"Select Destination for ".join(selected_companies), dests)
    #     if selected_destination:
    #         url = f"http://localhost:6800/schedule.json"
    #         data = {
    #             'project': 'default',
    #             'spider': company.lower(),
    #             "depart":selected_departure,
    #             "destination":selected_destination
    #         }
    #         requests.post(url, data=data)
    #         tarif = pd.DataFrame(list(db[f"tarif_{company.lower()}"].find({},{"_id":0})))
    #         st.write(tarif)
    #         db[f"tarif_{company.lower()}"].delete_many({})
    # available_destinations = destinations_map[selected_departure]
#     selected_destination = st.selectbox("Select Destination", available_destinations)

# Display selected values
# if st.button("Submit"):
#     st.write(f"You selected: Departure - {selected_departure}, Destination - {selected_destination}")
# if st.button("Get Data"):

#     url = "http://localhost:6800/schedule.json"
#     data_soretras = {
#         'project': 'default',
#         'spider': 'soretras',
#         "depart":depart,
#         "destination":destination
#     }
#     data_srtm = {
#         'project': 'default',
#         'spider': 'srtm',
#         "depart":depart,
#         "destination":destination
#     }
#     requests.post(url, data=data_soretras)
#     requests.post(url, data=data_srtm)
# soretras = pd.DataFrame(list(tarif_soretras.find({},{"_id":0})))
# srtm = pd.DataFrame(tarif_srtm.find({},{"_id":0}))
# df = pd.concat([soretras,srtm],axis=0)
# st.write(df)
# tarif_srtm.delete_many({})
# tarif_soretras.delete_many({})

    
        
