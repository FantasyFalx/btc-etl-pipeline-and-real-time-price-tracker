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
        return f"{message} was consumed and removed from the queue."
    return _consume_message

@pytest.fixture
def producer_callable_raises():
    calls = {"count": 0}
    def _produce():
        calls["count"] += 1
        if calls["count"] == 1:
            return {"ticker": "BTC-USD", "price": 100000}
        raise ConnectionError("socket closed")  # triggers except → event.set()
    return _produce


