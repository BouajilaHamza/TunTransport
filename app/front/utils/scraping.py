import json
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
    



@st.cache_resource(show_spinner=False)
def get_tarifs(location_name:str, location_id:str, company:str)-> json:
    
    url = "http://localhost:6800/schedule.json"
    payload = {
        'project': 'default',
        'spider': 'tarifs',
        "depart":location_name,
        "location_id":location_id,
        "Company":company
    }
    response = requests.post(url, data=payload)

    return response.json()


@st.cache_resource(show_spinner=False)
def wait_for_spider(response:json):
    job_id = response["jobid"]
    while True:
        time.sleep(3)
        url = f"http://localhost:6800/status.json?job={job_id}"

        payload = {
            "project": "default",
        }
        result = requests.get(url, data=payload)
        result = dict(result.json())
        if result.get("status") == "ok":
            return True

