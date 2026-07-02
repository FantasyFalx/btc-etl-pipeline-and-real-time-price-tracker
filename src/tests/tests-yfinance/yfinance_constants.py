# Standard libraries
# 3rd party
# Custom modules

# Constants
YFINANCE_TEST_TICKER = "BTC-USD"

## Mock Paths ##
MOCK_PATHS = {
    "websocket_listen": "btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket.listen",
    "websocket_subscribe": "btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket.subscribe",
    "websocket": "btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket",
    "validate_message": "btc_streaming_etl.pubsub.data_validator.DataValidator.validate_message",
}

VALID_YFINANCE_BTC_MESSAGE = {
    "id": YFINANCE_TEST_TICKER,
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

INVALID_YFINANCE_BTC_MESSAGE = {
    "id": 123,
    "price": "75751.76",
    "time": 1777478204000,
    "currency": "USD",
    "exchange": "CCC",
    "quote_type": "41",
    "market_hours": "open",
    "change_percent": "-0.3956858",
    "day_volume": 34821365760,
    "day_high": "77881.66",
    "day_low": "75734.74",
    "change": "-300.9297",
    "open_price": "76340.38",
    "last_size": 34821365760,
    "price_hint": 2,
    "vol_24hr": 34821365760,
    "vol_all_currencies": None,
    "from_currency": 999,
    "circulating_supply": "20022372.0",
}


def mock_callable(message: dict) -> dict:
    return message
