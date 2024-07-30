import requests
import time
import streamlit as st


# @st.cache_resource(show_spinner=False)
def get_departs():
    url = "http://localhost:6800/schedule.json"
    payload = {
        'project': 'default',
        'spider': 'dests',
    }
    response = requests.post(url, data=payload)
    time.sleep(15)
    
    
    
    
    
@st.cache_resource(show_spinner=False)
def get_available_destinations(depart_name:str, depart_id:str, depart_company:str):
    
    url = "http://localhost:6800/schedule.json"
    payload = {
        'project': 'default',
        'spider': 'deps',
        "depart":depart_name,
        "dep_id":depart_id,
        "Company":depart_company
    }
    response = requests.post(url, data=payload)
    time.sleep(10)
    

