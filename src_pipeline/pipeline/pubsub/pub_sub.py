# Standard libraries
import json
from datetime import datetime
import time
import logging
from urllib.error import HTTPError
# 3rd party
from pycoingecko import CoinGeckoAPI
from google.cloud import pubsub_v1
from google.cloud import secretmanager
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
# Custom modules
from configs.configs import GECKO_SECRET_URI, PUB_SUB_SA_SECRET_URI, PROJECT_ID, TOPIC_ID


try:
    logging.info("Creating GCP secret manager client")
    secret_client = secretmanager.SecretManagerServiceClient()
    logging.info("Creating CoinGecko API Client")
    gecko_secret = secret_client.access_secret_version(name=GECKO_SECRET_URI)
    coin_client = CoinGeckoAPI(demo_api_key=gecko_secret.payload.data.decode("UTF-8"))
    logging.info("Successfully created CoinGecko API Client.") 
    logging.info("Creating Pub/Sub client")
    pub_sub_sa_secret = secret_client.access_secret_version(name=PUB_SUB_SA_SECRET_URI)
    pub_sub_credentials = service_account.Credentials.from_service_account_info(json.loads(pub_sub_sa_secret.payload.data.decode("UTF-8")))
    pub_sub_client = pubsub_v1.PublisherClient(credentials=pub_sub_credentials)
    logging.info("Successfully created Pub/Sub client.")
except HttpError as e:
    logging.error("Error during client(s) initialization: %s. Please check key status and network connectivity.", e)
    raise
    

def payload_creator() -> str:
    """Creates a payload message for BTC utilizing coingecko API, to send BTC price data as a pub/sub message 
    over GCP. 

    Returns:
        str: Returns a json object in a string format, so json object can be transferred as a pub/sub message. 
    """
    try: 
    
     
        btc_price = coin_client.get_price(ids="bitcoin", vs_currencies="usd").get("bitcoin").get("usd")
        coin_data = coin_client.get_coin_by_id(id="bitcoin", vs_currencies="usd")

        btc_volume = coin_data.get("market_data").get("total_volume").get("usd")
        event_type = "GET"
        event_time = str(datetime.now())
        event_date = datetime.strftime(datetime.now().date(), "%Y-%m-%d")

        event_data = {
            "event_type": event_type,
            "event_date": event_date,        
            "event_time": event_time,
            "api_url": coin_client.api_base_url,
            "btc_price": btc_price,
            "btc_volume": btc_volume
        }

        payload_message = json.dumps(event_data)
    
        return payload_message
    except HTTPError as e:
        logging.error("HTTPError when fetching coin data: %s", e)
        logging.error("Error %s, has occurred. Coin Gecko api is denying your requests.", e)
        logging.error("Blank data will only be present, until requests are accepted. by server.")
        return json.dumps({}) # Return empty dict on API call failure
        

def pub_sub_publisher() -> None:
    topic_path = pub_sub_client.topic_path(
        PROJECT_ID, 
        TOPIC_ID,
    )
    payload = payload_creator()
    data = payload.encode("utf-8")
    future = pub_sub_client.publish(topic_path, data)
    time.sleep(5)
    logging.info(future.result())
    logging.info("Published to topic %s", topic_path)
    
def publish_tester() -> None:
    for i in range(100):
     print(f"Run: {i}")
     pub_sub_publisher()
     
def publisher_production_runner() -> None:
    message_number = 0
    while True: 
        message_number += 1
        logging.info("Run: %s", message_number)
        print(f"Message: {1}", message_number)
        pub_sub_publisher()
    
if __name__ == "__main__":
   # Production runs:
   publisher_production_runner()
  
  # Test runs: 
   #publish_tester()

    
    