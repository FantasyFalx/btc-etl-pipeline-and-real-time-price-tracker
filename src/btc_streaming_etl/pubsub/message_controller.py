"""Message controller module for coordinating streaming, threading, and publishing."""

## IMPORTS ##
# STANDARD LIBRARIES
# 3RD PARTY LIBRARIES
# CUSTOM IMPORTS
from btc_streaming_etl.pubsub.thread_manager import ThreadManager
from btc_streaming_etl.pubsub.pubsub_publisher import PubSubPublisher
from btc_streaming_etl.pubsub.yfinance_manager import YFinanceManager

##############

TICKER = "BTC-USD"


def execute_stream() -> None:

    ## Setting up the yfinance manager and ticker
    yfinance = YFinanceManager()
    yfinance.set_ticker(TICKER)
    ##

    ## Setting up the publisher client and topic path
    publisher = PubSubPublisher()
    publisher.set_publisher_client()
    publisher.set_topic_path()
    ##

    ## Starts the threading manager and executes the threads
    thread_manager = ThreadManager(yfinance, publisher)
    thread_manager.execute_threads()
    ##


if __name__ == "__main__":
    execute_stream()
else:
    None
