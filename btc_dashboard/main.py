# Standard Libary
from datetime import datetime
import time
import logging
# 3rd Party
import streamlit as st
from googleapiclient.errors import HttpError
import altair as alt
from millify import millify
# Custom Modules
from configs.resources import secret_puller, SIMPLE_METRICS_QUERY, PRICE_TIME_QUERY
from utils.data_puller import get_data, bq_client_creator

# Runtime Constants
PROJECT_ID = st.secrets["PROJECT_ID"]

try:
    logging.info("Getting secret for client connection.")
    secret = secret_puller()
    logging.info("Secret created")
    logging.info("Creating client connection")
    client = bq_client_creator(secret, PROJECT_ID)
    logging.info("Client connection created")
except HttpError as e:
    logging.error("Error: %s", e)
    logging.error("Client connection failed.")

st.cache_data(ttl=80)
def chart_data_cache():
    data = get_data(client, PRICE_TIME_QUERY, PROJECT_ID)
    return data

st.cache_data(ttl=240)
def simple_metric_cache():
    data = get_data(client, SIMPLE_METRICS_QUERY, PROJECT_ID)
    return data

# Placeholders for rendering containers on price/ metric updates.
placeholder_1 = st.empty()
placeholder_2 = st.empty()
placeholder_3 = st.empty()
placeholder_4 = st.empty()

def main():
    
    while True: 
        
        try: 
            logging.info("Pulling chart and metrics data from big query.")
            chart_data = chart_data_cache()
            metric_data = simple_metric_cache()
            logging.info("Data pulled from big query.")
        except HttpError as e:
            logging.error("Failed pulling data from big query.")
            st.error(f"Error: {e}")
            break
        
        # Live price tracking chart configurations.("Chart creation was assisted by gemini. ")
        chart = alt.Chart(chart_data).mark_line().encode(
            x=alt.X("event_time:T", axis=alt.Axis(format="%H:%M", tickCount="hour", title="Time in Minutes")),
            y=alt.Y("btc_price:Q", scale=alt.Scale(zero=False), axis=alt.Axis(title="Price in USD")),
            tooltip=["btc_price"]
        )
        
        # Extracts metrics from query.
     
        try:
            min_price = metric_data["btc_min_price"].min()
            max_price = metric_data["btc_max_price"].max()
            avg_price = metric_data["btc_average_price"].mean()
            volume = metric_data["btc_volume"].mean()
            price_change = metric_data["btc_price_change"].tail(1).values[0] # Most recent price update
        except IndexError as i:
            price_change = 0
            min_price = 0
            max_price = 0
            avg_price = 0
            volume = 0
            logging.error("Error: %s", i)
            
        
        # Date extracts for dashboard formatting. 
        current_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        
        with placeholder_1.container(horizontal=True, width=700, horizontal_alignment="center"):
            with st.container(horizontal=True, width=700, horizontal_alignment="center"):
                st.title("₿ Bitcoin Price Dashboard ₿", text_alignment="center")
                st.subheader(f"Live Price Updates Per Minute for {current_date}", text_alignment="center")
            with placeholder_2.container(horizontal=True, width=700, horizontal_alignment="center"):
                st.altair_chart(chart, width="stretch")
        with placeholder_3.container(width=1500, horizontal_alignment="center", gap="medium", horizontal=True):
            st.subheader("Key Metrics", text_alignment="center")
        with placeholder_4.container(horizontal=True, width=1500, horizontal_alignment="center"):
            col1, col2, col3, col4, col5 = st.columns(5, width="stretch")
            with col1:
                with st.container(border=True):
                    st.metric(label="Minimum Price",value=millify(min_price, precision=1))
            with col2:
                with st.container(border=True):
                    st.metric(label="Maximum Price", value=millify(max_price, precision=1))
            with col3:
                with st.container(border=True):
                    st.metric(label="Average Price", value=millify(avg_price, precision=1))
            with col4:
                with st.container(border=True):
                    st.metric(label="Volume", value=millify(volume))
            with col5:
                with st.container(border=True):
                    st.metric(label="Price Changes", value=millify(price_change))
                
        # Resets the components to pull the most recent data        
        time.sleep(60)
        placeholder_2.empty()
        placeholder_4.empty()
                
if __name__ == "__main__":
    main()
