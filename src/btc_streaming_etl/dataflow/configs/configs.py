# GCLOUD RUN CONFIGS/ PIPELINE COMMANDS
TOPIC = "projects/bitcoin-streaming-etl-project/topics/btc_price_topic"
SUBSCRIPTION = "projects/bitcoin-streaming-etl-project/subscriptions/btc_pull_topic"
PROJECT_ID = "bitcoin-streaming-etl-project"
REGION = "us-central1"
SERVICE_ACCOUNT_EMAIL = (
    "data-flow-9999@bitcoin-streaming-etl-project.iam.gserviceaccount.com"
)
STAGING_LOCATION = "gs://staging-bucket-88888/staging"
TEMP_LOCATION = "gs://staging-bucket-88888/tmp"

## runner options: DataflowRunner, DirectRunner
RUNNER = "DataflowRunner"
DIRECT_RUNNER = "DirectRunner"
SETUP_FILE = "./configs/setup.py"
LOCAL_FILE = "./src/btc_streaming_etl/dataflow/pipeline.py"

SAVE_MAIN_SESSION = True
ENABLE_PRE_FLIGHT_VALIDATION = False


PIPELINE_OPTIONS = {
    "project": PROJECT_ID,
    "region": REGION,
    "service_account_email": SERVICE_ACCOUNT_EMAIL,
    "staging_location": STAGING_LOCATION,
    "temp_location": TEMP_LOCATION,
    "runner": DIRECT_RUNNER,
    "setup_file": LOCAL_FILE,
    "save_main_session": SAVE_MAIN_SESSION,
}

# BIG QUERY CONFIGS
TABLE_SCHEMA = """
    id:STRING, price:FLOAT, time:STRING, currency:STRING, exchange:STRING,
    quote_type:INTEGER, market_hours:INTEGER, change_percent:FLOAT,
    day_volume:STRING, day_high:FLOAT, day_low:FLOAT, change:FLOAT,
    open_price:FLOAT, last_size:STRING, price_hint:STRING, vol_24hr:STRING,
    vol_all_currencies:STRING, from_currency:STRING, circulating_supply:FLOAT,
    market_cap:FLOAT
"""

OUTPUT_TABLE = "bitcoin-streaming-etl-project.bitcoin_streaming_dataset.bitcoin-data-streaming-table"

PACKAGES = ["apache-beam[gcp]", "apache-beam"]

CONFIGS = {
    "topic": TOPIC,
    "schema": TABLE_SCHEMA,
    "output_table": OUTPUT_TABLE,
    "pipeline_options": PIPELINE_OPTIONS,
    "subscription": SUBSCRIPTION,
    "project_id": PROJECT_ID,
    "region": REGION,
    "service_account_email": SERVICE_ACCOUNT_EMAIL,
    "staging_location": STAGING_LOCATION,
    "temp_location": TEMP_LOCATION,
    "runner": RUNNER,
    "setup_file": SETUP_FILE,
    "save_main_session": SAVE_MAIN_SESSION,
    "enable_preflight_validation": ENABLE_PRE_FLIGHT_VALIDATION,
}

##################################################################################
