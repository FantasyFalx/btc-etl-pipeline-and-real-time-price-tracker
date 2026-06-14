# IMPORT STANDARD LIBRARIES
import threading
from queue import Queue, Empty
import logging
import concurrent.futures
import time

# IMPORT 3RD PARTY LIBRARIES

# IMPORT CUSTOM LIBRARIES
from btc_streaming_etl.pubsub.yfinance_manager import YFinanceManager

"""I will import pub/sub .py file later."""


logging.basicConfig(level=logging.INFO)

## This makes no sense because the yfinance manager is running the socket and the thread manager is running the thread.
# Why add unnecessary complexity?
## Thread manager will be run in the yfinance manager.

# Set types later for the objects.


class ThreadManager:
    def __init__(self, producer_object: YFinanceManager, consumer_object: callable):
        self.thread: threading.Thread | None = None
        self.thread_running: bool = False
        self.event: threading.Event = threading.Event()
        self.message_queue: Queue = Queue(maxsize=1000)
        self.SENTINEL = None
        # The produce needs to be changed to a yfinance manager.
        self.producer_object = producer_object
        self.consumer_object = consumer_object

    """
    Components:
     - Event, pool manager, and queue.
     - Consume collects the messages. 
     - Producer produces the messages. 
     # Ref link: 
     https://realpython.com/intro-to-python-threading/#producer-consumer-threading
    """

    def execute_threads(self) -> None:

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_producer = executor.submit(
                self.producer, self.message_queue, self.event
            )

            future_consumer = executor.submit(
                self.consumer, self.message_queue, self.event
            )

            concurrent.futures.wait(
                [future_producer, future_consumer],
                # timeout=5,
                return_when=concurrent.futures.ALL_COMPLETED,
            )

    def producer(self, queue: Queue, event: threading.Event) -> None:

        try:
            # message = self.producer_object()
            # queue.put(message)
            # print(queue.qsize())
            ###
            self.producer_object.run_socket(self.queue_gluer)
            ###
        except Exception as e:
            event.set()
            ### Puts a sentinel value into the queue to signal the consumer to stop.
            queue.put(self.SENTINEL)
            logging.error(f"Error in producer: {e}")
        finally:
            # for tests.
            event.set()

    def queue_gluer(self, message: dict) -> None:
        new_message = self.producer_object.message_handler(message)
        if new_message:
            self.message_queue.put(new_message)

    ## Fix the logic later.
    def consumer(self, queue: Queue, event: threading.Event) -> None:
        while not event.is_set() or not queue.empty():
            try:
                message = queue.get(timeout=0.1)
                self.consumer_object(message)
            except Empty:
                continue

            if message is self.SENTINEL:
                break
