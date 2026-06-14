"""File for storing creating credential objects for service account use in development. 
"""

# Imports
from google.oauth2.service_account import Credentials


# PATH LINKS
# Change these back to relative paths one the real development begins.
BIG_QUERY_CRED = "./big_query_key.json"
CLOUD_STORAGE_CRED = "./cloud_storage_key.json"
PUB_SUB_CRED = "./pub_sub_key.json"
CLOUD_MONITORING_CRED = "./cloud_monitoring_key.json"
DATA_FLOW_CRED = "./data_flow_key.json"


DEV_CREDS = {
    "big_query": Credentials.from_service_account_file(BIG_QUERY_CRED),
    "cloud_stroage": Credentials.from_service_account_file(CLOUD_STORAGE_CRED),
    "pub_sub": Credentials.from_service_account_file(PUB_SUB_CRED),
    "cloud_monitoring": Credentials.from_service_account_file(CLOUD_MONITORING_CRED),
    "data_flow": Credentials.from_service_account_file(DATA_FLOW_CRED)
}



