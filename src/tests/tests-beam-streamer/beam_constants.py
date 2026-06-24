"""Test constants for Apache Beam Dataflow pipeline module tests."""

## IMPORTS ##
# STANDARD LIBRARIES
# 3RD PARTY LIBRARIES
# CUSTOM IMPORTS
##############

## Mock Paths ##
MOCK_PATHS = {
    "read_from_pubsub": "apache_beam.io.ReadFromPubSub",
    "write_to_bigquery": "apache_beam.io.WriteToBigQuery",
}

## Mock Data ##
MOCK_MESSAGE = {
    "id": "BTC-USD",
    "price": 75751.76,
    "time": "1777478204000",
    "currency": "USD",
    "exchange": "CCC",
    "quote_type": 41,
    "market_hours": 1,
    "change_percent": -0.3956858,
    "day_volume": "34821365760",
    "day_high": 77881.66,
    "day_low": 75734.74,
    "change": -300.9297,
    "open_price": 76340.38,
    "last_size": "34821365760",
    "price_hint": "2",
    "vol_24hr": "34821365760",
    "vol_all_currencies": "34821365760",
    "from_currency": "BTC",
    "circulating_supply": 20022372.0,
    "market_cap": 1516389140000.0,
}


if __name__ == "__main__":
    None
else:
    None
