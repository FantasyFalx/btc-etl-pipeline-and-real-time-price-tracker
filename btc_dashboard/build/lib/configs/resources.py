# Standard libraries
import logging
import json
# 3rd party imports
from google.cloud import secretmanager
from googleapiclient.errors import HttpError
# Custom Modules

# RESOURCES CONSTANTS
PROJECT_ID = "862053225903"
BQ_SECRET_RESOURCE = "projects/862053225903/secrets/big_query_secret/versions/1"

# QUERIES
PRICE_TIME_QUERY = r"""
    SELECT 
    event_time, 
    btc_price
    FROM `bitcoin-streaming-etl-project.bitcoin_streaming_dataset.bitcoin-data-streaming-table`
    WHERE 
        event_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) AND CURRENT_DATE()
        ORDER BY event_time ASC
    limit 100
"""

SIMPLE_METRICS_QUERY = r"""
    SELECT 
    btc_min_price, 
    btc_max_price, 
    btc_average_price, 
    btc_volume, 
    btc_price_change
    FROM `bitcoin-streaming-etl-project.bitcoin_streaming_dataset.bitcoin-data-streaming-table`
    WHERE 
        event_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) AND CURRENT_DATE()
        ORDER BY event_time ASC
    limit 100
"""

# SECRET PULLER FUNCTION
def big_query_secret() -> dict:
    secret_client = secretmanager.SecretManagerServiceClient()
    response = secret_client.access_secret_version(name=BQ_SECRET_RESOURCE)
    # Needs to be an object with attribute keys, so a dict. This was just a string. 
    return json.loads(response.payload.data.decode('UTF-8'))


    
