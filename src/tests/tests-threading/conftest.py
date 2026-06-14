# Standard libraries

# 3rd party
import pytest

# Custom modules
from btc_streaming_etl.pubsub.thread_manager import ThreadManager
from btc_streaming_etl.pubsub.yfinance_manager import YFinanceManager



@pytest.fixture
def yfinance_manager_factory(mocker):
    mocker.patch(
        "btc_streaming_etl.pubsub.yfinance_manager.YFinanceManager.run_socket",
        new=mocker.MagicMock()
    )
    return YFinanceManager()


@pytest.fixture
def thread_manager_factory(yfinance_manager_factory: YFinanceManager):
    return lambda producer_object, consumer_object: ThreadManager(
        producer_object=producer_object, 
        consumer_object=consumer_object
    )

@pytest.fixture
def producer_callable():
    def _produce():
        return {"ticker": "BTC-USD", "price": 50000}
    return _produce

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


