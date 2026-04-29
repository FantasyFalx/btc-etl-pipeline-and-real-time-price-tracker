## Standard libraries
from urllib.error import HTTPError
from websockets.exceptions import ConnectionClosed

# 3rd party
import pytest

# Custom modules
from constants import (
    TEST_TICKER,
    VALID_YFINANCE_BTC_MESSAGE,
    INVALID_YFINANCE_BTC_MESSAGE,
)

# Functions
def test_set_ticker_success(mock_ticker, yfinance_manager_factory):
    manager = yfinance_manager_factory
    manager.set_ticker(mock_ticker)
    assert manager.ticker == mock_ticker

def test_set_socket_success(mock_yfinance_set_socket, mock_socket):
    manager = mock_yfinance_set_socket
    manager.set_socket()
    assert manager.socket == mock_socket

def test_handler(mock_handler_message, yfinance_manager_factory):
    manager = yfinance_manager_factory
    message = manager.message_handler(mock_handler_message)
    assert message == mock_handler_message

def test_socket_failure(mock_closed_connection):
    manager = mock_closed_connection
    with pytest.raises(ConnectionClosed):
        manager.run_socket()

def test_missing_ticker_error(mock_missing_ticker_error):
    manager = mock_missing_ticker_error
    with pytest.raises(TypeError):
        manager.run_socket()

def test_invalid_ticker_error(mock_invalid_ticker_error):
    manager = mock_invalid_ticker_error
    with pytest.raises(ValueError):
        manager.run_socket()

def test_yfinance_successful_run_socket(mock_yfinance_successful_run_socket):
    manager = mock_yfinance_successful_run_socket
    manager.set_ticker(TEST_TICKER)
    manager.run_socket()
    manager.socket.subscribe.assert_called_once_with(TEST_TICKER)
    manager.socket.listen.assert_called_once_with(manager.message_handler)

def test_schema_validator_success(yfinance_manager_factory):
    manager = yfinance_manager_factory
    assert manager.schema_validator(VALID_YFINANCE_BTC_MESSAGE) is True