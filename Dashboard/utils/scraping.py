import json
import os
import time
from typing import Annotated, List

import requests
import streamlit as st

SCRAPING_URI = os.getenv("SCRAPING_URI")


# @st.cache_resource(show_spinner=False)
def get_departs():
    url = f"{SCRAPING_URI}/schedule.json"
    payload = {
        "project": "default",
        "spider": "deps",
    }
    response = requests.post(url, data=payload)
    time.sleep(15)
    return response


@st.cache_resource(show_spinner=False)
def get_available_destinations(depart_name: str, depart_id: str, depart_company: str):
    url = f"{SCRAPING_URI}/schedule.json"
    payload = {
        "project": "default",
        "spider": "dests",
        "depart": depart_name,
        "dep_id": depart_id,
        "Company": depart_company,
    }
    response = requests.post(url, data=payload)
    return response


# @st.cache_resource(show_spinner=False)
def get_tarifs(
    _depart: dict, _destination: dict, company: Annotated[str, List[str]]
) -> json:
    url = f"{SCRAPING_URI}/schedule.json"
    payload = {
        "project": "default",
        "spider": "tarifs",
        "depart": json.dumps(_depart),
        "destination": json.dumps(_destination),
        "Company": company,
    }
    response = requests.post(url, data=payload)

    return response.json()


@st.cache_resource(show_spinner=False)
def wait_for_spider(response: json):
    job_id = response["jobid"]
    while True:
        time.sleep(3)
        url = f"{SCRAPING_URI}/status.json?job={job_id}"

        payload = {
            "project": "default",
        }
        result = requests.get(url, data=payload)
        result = dict(result.json())
        if result.get("status") == "ok":
            return True
