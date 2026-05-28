# Standard libraries

# 3rd party
import pytest

# Custom modules
from btc_streaming_etl.pubsub.thread_manager import ThreadManager


@pytest.fixture
def thread_manager_factory():
    return lambda producer, consumer: ThreadManager(producer, consumer)


@pytest.fixture
def producer_callable():
    return lambda: {
        "ticker": "BTC-USD",
        "price": 100000,
        "timestamp": "2026-05-28 12:00:00",
    }


# Fix these later. 
@pytest.fixture
def consumer_callable():
    def _consume_message(message):
        print(f"Consumer message: {message}")
    return _consume_message


