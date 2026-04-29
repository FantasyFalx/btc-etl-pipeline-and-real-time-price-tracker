# Standard libraries
import logging
import json
# 3rd party imports
import streamlit as st
from google.cloud import secretmanager
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
# Custom Modules

# RESOURCES CONSTANTS

# QUERIES
PRICE_TIME_QUERY = r"""
    SELECT 
    event_time, 
    btc_price FROM (
        SELECT 
            event_time, 
            btc_price
        FROM `bitcoin-streaming-etl-project.bitcoin_streaming_dataset.bitcoin-data-streaming-table`
        WHERE 
            event_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) AND CURRENT_DATE()
        ORDER BY event_time DESC
        LIMIT 100
    )
    ORDER BY event_time ASC;
"""

SIMPLE_METRICS_QUERY = r"""
    SELECT 
        btc_min_price, 
        btc_max_price, 
        btc_average_price, 
        btc_volume, 
        btc_price_change
    FROM (
        SELECT 
            btc_min_price, 
            btc_max_price, 
            btc_average_price, 
            btc_volume, 
            btc_price_change,
            event_time
        FROM `bitcoin-streaming-etl-project.bitcoin_streaming_dataset.bitcoin-data-streaming-table`
        WHERE event_date = CURRENT_DATE()
        ORDER BY event_time DESC
        LIMIT 100
    )
    ORDER BY event_time ASC
"""

# SECRET PULLER FUNCTION
def secret_puller() -> dict:
    credentials = service_account.Credentials.from_service_account_info(st.secrets["SECRET_MANAGER_SA_KEY"])
    secret_client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    response = secret_client.access_secret_version(name=st.secrets["BIG_QUERY_RESOURCE"])
    return json.loads(response.payload.data.decode('UTF-8'))


    
