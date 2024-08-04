import time
import streamlit as st
from utils.database import init_mongo,get_dests_from_mongo
from utils.scraping import get_departs,get_tarifs,wait_for_spider
from utils.ETL import clean_filter
import pandas as pd
st.set_page_config(page_title="Transport Booking System", page_icon="🚗", layout="wide")


collection , dests,tarif_collection = init_mongo()
raw_data,data = clean_filter(collection,{})
st.title("Transport Booking System 🚗")
st.write("This is a simple web application that allows you to book your transport ticket online")
st.write("The data is fetshed directly from the companies **Official** websites")
selected_companies = st.multiselect("Select Company", ["SRTM", "SRTG", "Soretras"])
if selected_companies:
    filter = {"Company": {"$in": selected_companies}} if selected_companies else {}
    raw_data,data = clean_filter(collection,filter)
    if len(data) == 0:
        st.info("No data available for the selected companies We will get the data from the web")
        with st.spinner("Getting data from the web ..."):
            get_departs()
            raw_data,data = clean_filter(collection,filter)
            selected_departure = st.selectbox("Select Departure Station", data,key="depart")
            if selected_departure:
                
                selected_dict = [i for i in raw_data if i["Name"]==selected_departure]
                if len(selected_dict) == 0:
                    st.info(selected_dict)
                else:
                    selected_dict = selected_dict[0]
                raw_dests,clean_dests = get_dests_from_mongo(dests, selected_dict, selected_companies)
                selected_dests = st.selectbox("Select Destination", clean_dests)
    else:
        selected_departure = st.selectbox("Select Departure Station", data,key="depart")
        if selected_departure:
            selected_dict = [i for i in raw_data if i["Name"]==selected_departure]
            if len(selected_dict) == 0:
                st.info(selected_dict)
            else:
                selected_dict = selected_dict[0]
            raw_dests,clean_dests = get_dests_from_mongo(dests, selected_dict, selected_companies)
            selected_dest = st.selectbox("Select Destination", clean_dests)
            
            if selected_dest :
                selected_dest_dicts = [i for i in raw_dests if i["Name"]==selected_dest]
                if len(selected_dest_dicts) == 0:
                    st.info("No data available for the selected destination")
                else:
                    with st.spinner("Getting Tarification from the web ..."):
                        selected_dest_dict = selected_dest_dicts[0]
                        available_tarifs = list(tarif_collection.find({"depart":selected_departure,"destination":selected_dest}, {"_id":0}))
                        if len(available_tarifs) == 0:   
                            response = get_tarifs(selected_dict, selected_dest_dict, selected_dest_dict["Company"])
                            wait_for_spider(response)
                            filter = {"depart":selected_departure,"destination":selected_dest}
                            _,_,tarif_collection = init_mongo()
                            l=list(tarif_collection.find(filter,{"_id":0}))
                            df = pd.DataFrame(l)
                        else:
                            l=list(available_tarifs)
                            df = pd.DataFrame(l)
                        with st.container():
                            st.dataframe(df,hide_index=True,use_container_width=True)

                        st.info("S'il ya une fausse donnée ou une donné monquante, veuillez les signaler\nou l'ajouter\nNous avons besoin de votre aide pour améliorer notre service\nMerci pour votre compréhension\nNous allons vérifier votre demande et vous répondre dans les plus brefs délais")
                        form_holder = st.form("form")
                        with form_holder:
                            col_dep,col_dest = st.columns(2)
                            col_dep.selectbox("Select Departure Station", data,key="depart_input")
                            col_dest.selectbox("Select Destination", clean_dests,key="dest_input")
                            coldep_time,colarr_time = st.columns(2)
                            coldep_time.time_input("Departure Time",key="dep_time")
                            colarr_time.time_input("Arrival Time",key="arr_time")
                            colprice = st.columns(1)
                            st.number_input("Price",key="price")
                            colcompany = st.columns(1)
                            st.selectbox("Select Company", selected_companies)
                            submit = st.form_submit_button("Submit")
                        if submit:
                            st.write("Form submitted")
   

    
    
    
    
    
    
    
    
    
    
