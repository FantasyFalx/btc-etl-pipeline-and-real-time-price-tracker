# Standard libraries


# 3rd party
import pytest
# Source - https://stackoverflow.com/a/3193387
# Posted by Tim Pietzcker, modified by community. See post 'Timeline' for change history
# Retrieved 2026-04-27, License - CC BY-SA 4.0
from websockets.exceptions import ConnectionClosed
# Custom modules
from btc_streaming_etl.pubsub.yfinance_manager import YFinanceManager
# Constants
from constants import VALID_YFINANCE_BTC_MESSAGE, INVALID_YFINANCE_BTC_MESSAGE
# Fixtures
@pytest.fixture
def yfinance_manager_factory():
    return YFinanceManager()

@pytest.fixture
def mock_socket(mocker):
    return mocker.MagicMock()

@pytest.fixture
def mock_ticker():
    return "BTC-USD"

@pytest.fixture
def mock_closed_connection(
    mocker, yfinance_manager_factory
):
    mocker.patch(
        "btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket.listen", 
        side_effect = ConnectionClosed(
            None, 
            None
        )
    )
    return yfinance_manager_factory

@pytest.fixture
def mock_missing_ticker_error(mocker, yfinance_manager_factory):
    mocker.patch(
        "btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket.subscribe",
        side_effect = TypeError(
            "Test error for if the ticker is None."
        )
    )
    return yfinance_manager_factory

@pytest.fixture
def mock_invalid_ticker_error(mocker, yfinance_manager_factory):
    mocker.patch(
        "btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket.subscribe",
        side_effect = ValueError(
            "Test error for if the ticker is invalid."
        )
    )
    return yfinance_manager_factory


@pytest.fixture
def mock_yfinance_set_socket(mocker, mock_socket, yfinance_manager_factory):
    mocker.patch(
        "btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket",
        return_value=mock_socket
    )
    return yfinance_manager_factory

@pytest.fixture 
def mock_yfinance_successful_run_socket(
    mocker, mock_socket, 
    yfinance_manager_factory
):
    mocker.patch(
        "btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket",
        return_value=mock_socket
    )
    mock_socket.subscribe.return_value = True
    mock_socket.listen.return_value = True
    return yfinance_manager_factory


@pytest.fixture
def mock_schema_validator_failure(mocker, yfinance_manager_factory):
    mocker.patch(
        "btc_streaming_etl.pubsub.data_validator.DataValidator.validate_message",
        return_value=False,
    )
    return yfinance_manager_factory

@pytest.fixture
def mock_schema_validator_success(mocker, yfinance_manager_factory):
    mocker.patch(
        "btc_streaming_etl.pubsub.data_validator.DataValidator.validate_message",
        return_value=True
    )
    return yfinance_manager_factory


@pytest.fixture
def mock_failed_handler(mocker, yfinance_manager_factory):
    mocker.patch(
        "btc_streaming_etl.pubsub.data_validator.DataValidator.validate_message",
        return_value=False
    )
    return yfinance_manager_factory

## Queue Fixtures 

def fake_listen_success(callback):
    callback(VALID_YFINANCE_BTC_MESSAGE)
    return True

@pytest.fixture
def mock_yfinance_message_queue_success(mocker, yfinance_manager_factory):
    mocker.patch(
        "btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket.listen", 
        side_effect=fake_listen_success
    )
    return yfinance_manager_factory


def fake_listen_empty(callback):
    callback(None)
    return True

@pytest.fixture
def mock_yfinance_message_queue_empty(mocker, yfinance_manager_factory):
    mocker.patch(
        "btc_streaming_etl.pubsub.yfinance_manager.yf.WebSocket.listen", 
        side_effect=fake_listen_empty
    )
    return yfinance_manager_factory