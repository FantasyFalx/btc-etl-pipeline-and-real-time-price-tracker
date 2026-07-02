"""Configuration constants for Pub/Sub topics, GCP secrets, and schema validation keys."""

# Move to and env file or secrets.
PROJECT_ID = "bitcoin-streaming-etl-project"
GECKO_SECRET_URI = f"projects/{PROJECT_ID}/secrets/coingecko-api-key/versions/1"
PUB_SUB_SA_SECRET_URI = f"projects/{PROJECT_ID}/secrets/pub-sub-secret-key/versions/1"
TOPIC_ID = "btc_price_topic"
TOPIC = "projects/bitcoin-streaming-etl-project/topics/btc_price_topic"
SUBSCRIPTION = "projects/bitcoin-streaming-etl-project/subscriptions/btc_pull_topic"

# Valid keys for the schema validator.
# Utilize pydantic for the schema validation.
VALID_KEYS = [
    "id",
    "price",
    "time",
    "currency",
    "exchange",
    "quote_type",
    "market_hours",
    "change_percent",
    "day_volume",
    "day_high",
    "day_low",
    "change",
    "open_price",
    "last_size",
    "price_hint",
    "vol_24hr",
    "vol_all_currencies",
    "from_currency",
    "circulating_supply",
    "market_cap",
]
