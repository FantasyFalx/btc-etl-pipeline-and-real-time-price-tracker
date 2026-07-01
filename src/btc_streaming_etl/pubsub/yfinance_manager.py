"""YFinance manager module for WebSocket streaming, message handling, and schema validation."""

# Standard libraries
import logging
from websockets.exceptions import ConnectionClosed

# 3rd party
import yfinance as yf

# Custom modules
from btc_streaming_etl.pubsub.data_validator import DataValidator

logging.basicConfig(level=logging.INFO)


class YFinanceManager:
    def __init__(self):
        self.socket: yf.WebSocket | None = None
        self.ticker: str = None
        self.thread_running: bool = None

    def run_socket(self, handler: callable) -> None:
        try:
            self.set_socket()
            socket = self.socket
            socket.subscribe(self.ticker)
            socket.listen(handler)
        except ValueError as e:
            logging.error(f"Value error: {e}. Ticker cannot be None.")
            raise e
        except TypeError as e:
            logging.error(f"Type error: {e}. Invalid type for ticker.")
            raise e
        except ConnectionClosed as e:
            logging.error(f"Socket connection closed: {e}")
            raise e

    def set_socket(self) -> None:
        self.socket = yf.WebSocket()

    def set_ticker(self, ticker: str) -> None:
        self.ticker = ticker

    def message_handler(self, message: dict) -> dict | None:
        if self.is_valid_message(message):
            return message
        return None

    def is_valid_message(self, message: dict) -> bool:
        validator = DataValidator()
        return validator.validate_message(message)


if __name__ == "__main__":
    btc_manager = YFinanceManager()
    btc_manager.set_ticker("BTC-USD")
    btc_manager.run_socket(lambda msg: print(msg))
else:
    None
