# Standard Libraries
# 3rd Party Libraries
from google.cloud import bigquery
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.cloud import secretmanager
import pandas as pd
# Custom Modules

def bq_client_creator(key: dict, project_id: str) -> bigquery.Client:
    # Set the credentials with the client key
    creds = service_account.Credentials.from_service_account_info(key)
    client = bigquery.Client(credentials=creds, project=project_id)
    return client

def get_data(client: bigquery.Client, query: str, project_id: str) -> pd.DataFrame:
    query_job = client.query(query, project=project_id).to_dataframe()
    results = query_job
    return results
    