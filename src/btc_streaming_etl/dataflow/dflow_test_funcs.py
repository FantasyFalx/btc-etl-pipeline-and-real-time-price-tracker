# Standard Library
import json
# 3rd Party
import numpy as np
# Custom Modules

def fake_data_generator() -> dict:
    event_data = {
            "event_type": "price_event",
            "event_date": "else",        
            "event_time": "time",
            "api_url": "some_url",
            "btc_price": np.random.randint(100000),
            "btc_volume": np.random.randint(100000)
        }
    return event_data

def fake_data_compacter() -> dict:
    data = [fake_data_generator() for _ in range(10)]
    return data

def data_parser(message: str) -> list:
    data = json.loads(message)
    parsed_data = [
        ("event_type", data["event_type"]),
        ("event_date", data["event_date"]),
        ("event_time", data["event_time"]),
        ("btc_price", data["btc_data"]["price_usd"]),
        ("btc_volume", data["btc_data"]["btc_volume"])
    ]
    return parsed_data

def dict_unpacker(data):
    key = data.keys()
    value = data.values()
    return key, value
    