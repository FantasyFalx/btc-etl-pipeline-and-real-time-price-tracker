## Standard libraries
from websockets.exceptions import ConnectionClosed

# 3rd party
import pytest

# Custom modules
from constants import (
    TEST_TICKER,
    VALID_YFINANCE_BTC_MESSAGE,
    INVALID_YFINANCE_BTC_MESSAGE
)
from conftest import mock_callable

def test_set_ticker_success(mock_ticker, yfinance_manager_factory):
    manager = yfinance_manager_factory
    manager.set_ticker(mock_ticker)
    assert manager.ticker == mock_ticker

def test_set_socket_success(mock_yfinance_set_socket, mock_socket):
    manager = mock_yfinance_set_socket
    manager.set_socket()
    assert manager.socket == mock_socket

def test_schema_validator_success(mock_schema_validator_success):
    manager = mock_schema_validator_success
    assert manager.is_valid_message(VALID_YFINANCE_BTC_MESSAGE) is True

def test_schema_validator_failure(mock_schema_validator_failure):
    manager = mock_schema_validator_failure
    assert manager.is_valid_message(INVALID_YFINANCE_BTC_MESSAGE) is False


def test_missing_ticker_error(mock_missing_ticker_error):
    manager = mock_missing_ticker_error
    with pytest.raises(TypeError):
        manager.set_ticker(None)
        manager.run_socket()

def test_invalid_ticker_error(mock_invalid_ticker_error):
    manager = mock_invalid_ticker_error
    with pytest.raises(ValueError):
        manager.set_ticker(TEST_TICKER)
        manager.run_socket(mock_callable)

### TODO: Refactor these tests ###

def test_successful_handler(mock_schema_validator_success):
    manager = mock_schema_validator_success
    result = manager.message_handler(VALID_YFINANCE_BTC_MESSAGE)
    assert result == VALID_YFINANCE_BTC_MESSAGE

def test_failed_handler(mock_schema_validator_failure):
    manager = mock_schema_validator_failure
    result = manager.message_handler(INVALID_YFINANCE_BTC_MESSAGE)
    assert result is None

def test_socket_failure(mock_closed_connection):
    manager = mock_closed_connection
    with pytest.raises(ConnectionClosed):
        manager.set_ticker(TEST_TICKER) # Ticker is required before socket starts.
        manager.run_socket(mock_callable)

def test_yfinance_successful_run_socket(mock_yfinance_successful_run_socket):
    manager = mock_yfinance_successful_run_socket
    manager.set_ticker(TEST_TICKER)
    manager.run_socket(mock_callable)
    manager.socket.subscribe.assert_called_once_with(TEST_TICKER)
    manager.socket.listen.assert_called_once_with(mock_callable)

###########################################################