from btc_streaming_etl.pubsub.yfinance_manager import YFinanceManager
from btc_streaming_etl.pubsub.thread_manager import ThreadManager

yfinance = YFinanceManager()
yfinance.set_ticker("BTC-USD")

manager = ThreadManager(
    producer_object=yfinance, consumer_object=lambda msg: print(msg)
)

manager.execute_threads()  # runs until disconnect / Ctrl+C
