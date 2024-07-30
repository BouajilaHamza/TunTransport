import streamlit as st
from utils.database import init_mongo,get_dests_from_mongo
from utils.scraping import get_departs,get_available_destinations
from utils.ETL import clean_filter

collection , dests = init_mongo()
raw_data,data = clean_filter(collection,{})
st.title("Transport Booking System")
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
            selected_dests = st.selectbox("Select Destination", clean_dests)
# submit = st.button("Get Data")


    #     with st.spinner("Loading Destinations ..."):
#         dests.drop()
#         selected_dict = [i for i in raw_data if i["Name"]==selected_departure][0]
#         get_available_destinations(selected_departure, selected_dict["Id"], selected_dict["Company"])

#     dests =list(dests.find({},{"_id":0}))
#     dests = [i["Name"] for i in dests]
    
    
    
    
    
    
    
    # dests = dests[dests["Company"]==company]
    # dests = dests["Name"].unique()
    # dests = list(dests)
    # selected_destination = st.selectbox(f"Select Destination for ".join(selected_companies), dests)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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

    
        
