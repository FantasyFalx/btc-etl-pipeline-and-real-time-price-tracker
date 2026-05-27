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
    

    def get_message(self) -> dict | None:
        try:
            message = self.message_queue.popleft()
            print("I got the message.")
            return message
        except IndexError:
            return None
    
    
    def run_socket(self) -> None:
        try:
            self.set_socket()

            socket = self.socket
            socket.subscribe(self.ticker)
            socket.list(self.message_handler)
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

    
    # Redo these functions since I have added a threading class. 
    # The handler will return the message if its valid. 
    # Not add it to a queue. 
    def message_handler(self, message: dict) -> None:
        if self.is_valid_message(message):
            self.message_queue.append(message)
        
    def is_valid_message(self, message: dict) -> bool:
        validator = DataValidator()
        return validator.validate_message(message)
    

if __name__ == "__main__":
    btc_manager = YFinanceManager()
    btc_manager.set_ticker("BTC-USD")
    btc_manager.run_socket()
    while True:
        message = btc_manager.get_message()
        if message:
            print(f"Message: {message}")
        else:
            pass
else:
    None

