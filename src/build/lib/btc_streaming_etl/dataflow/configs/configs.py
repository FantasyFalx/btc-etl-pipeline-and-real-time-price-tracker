# DATAFLOW FILE CONFIGS ###############################################################

# LOCAL RUN CONFIGS/ PIPELINE COMMANDS
#| "Beam Create for local testing. " >> beam.Create(fake_data_compacter())
#options = PipelineOptions()
#options.view_as(StandardOptions).streaming = True

# GCLOUD RUN CONFIGS/ PIPELINE COMMANDS
TOPIC = "projects/bitcoin-streaming-etl-project/topics/btc_price_topic"
SUBSCRIPTION = "projects/bitcoin-streaming-etl-project/subscriptions/btc_pull_topic"
PROJECT_ID = "bitcoin-streaming-etl-project"
REGION = "us-central1"
SERVICE_ACCOUNT_EMAIL = "data-flow-9999@bitcoin-streaming-etl-project.iam.gserviceaccount.com"
STAGING_LOCATION = "gs://staging-bucket-88888/staging"
TEMP_LOCATION = "gs://staging-bucket-88888/tmp"
RUNNER = "DataflowRunner"
### Determine if set up file is needed later. 
SETUP_FILE = "./configs/setup.py"
#####
SAVE_MAIN_SESSION = True
ENABLE_PRE_FLIGHT_VALIDATION = False

PIPELINE_OPTIONS = {
    "project": PROJECT_ID,
    "region": REGION,
    "service_account_email": SERVICE_ACCOUNT_EMAIL,
    "staging_location": STAGING_LOCATION,
    "temp_location": TEMP_LOCATION,
    "runner": RUNNER,
    "setup_file": SETUP_FILE,
    "save_main_session": SAVE_MAIN_SESSION,
}

# BIG QUERY CONFIGS
TABLE_SCHEMA = """
    event_type:STRING, event_date:DATETIME, event_time:DATETIME,
    btc_price:FLOAT, btc_min_price:FLOAT, btc_max_price:FLOAT,
    btc_average_price:FLOAT, btc_volume:INTEGER, btc_price_change:INTEGER
"""
# Table resource locator for big query. 
OUTPUT_TABLE = "bitcoin-streaming-etl-project.bitcoin_streaming_dataset.bitcoin-data-streaming-table"

#options = PipelineOptions(flags=["--dataflow_service_options=enable_preflight_validation=false"], **PIPELINE_OPTIONS)
#options.view_as(StandardOptions).streaming = True

# SETUP UP TOOLS CONFIG
PACKAGES = [
    "apache-beam[gcp]",
    "apache-beam"
]

##################################################################################
