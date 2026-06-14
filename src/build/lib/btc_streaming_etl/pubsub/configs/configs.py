# PUB/SUB File Configs
# Put this into an env file. 
# Maybe cloud secretes who knows. 
PROJECT_ID = "bitcoin-streaming-etl-project"
GECKO_SECRET_URI = f"projects/{PROJECT_ID}/secrets/coingecko-api-key/versions/1"
PUB_SUB_SA_SECRET_URI = f"projects/{PROJECT_ID}/secrets/pub-sub-secret-key/versions/1"
TOPIC_ID = "btc_price_topic"
TOPIC = "projects/bitcoin-streaming-etl-project/topics/btc_price_topic"
SUBSCRIPTION = "projects/bitcoin-streaming-etl-project/subscriptions/btc_pull_topic"

