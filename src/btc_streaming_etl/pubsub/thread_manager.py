# IMPORT STANDARD LIBRARIES
import threading
from queue import Queue, Empty
import logging
import concurrent.futures
import json
import time

# IMPORT 3RD PARTY LIBRARIES

# IMPORT CUSTOM LIBRARIES
from btc_streaming_etl.pubsub.yfinance_manager import YFinanceManager
from btc_streaming_etl.pubsub.pubsub_publisher import PubSubPublisher

logging.basicConfig(level=logging.INFO)

class ThreadManager:
    def __init__(self, producer_object: YFinanceManager, consumer_object: PubSubPublisher):
        self.thread: threading.Thread | None = None
        self.thread_running: bool = False
        self.event: threading.Event = threading.Event()
        self.message_queue: Queue = Queue(maxsize=1000)
        self.SENTINEL = None
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

            logging.info(f"##### Executing threads #####\n")
            concurrent.futures.wait(
                [future_producer, future_consumer],
                return_when=concurrent.futures.ALL_COMPLETED,
            )

    def producer(self, queue: Queue, event: threading.Event) -> None:

        try:
            self.producer_object.run_socket(self.queue_gluer)
            
        except Exception as e:
            event.set()
            queue.put(self.SENTINEL)
            logging.error(f"Error in producer: {e}")
        finally:
            event.set()

    def queue_gluer(self, message: dict) -> None:
        new_message = self.producer_object.message_handler(message)
        if new_message:
            logging.info(f"##### Produced message #####\n")
            self.message_queue.put(new_message)
            logging.info(f"##### Queued message #####\n")

    def consumer(self, queue: Queue, event: threading.Event) -> None:
        while not event.is_set() or not queue.empty():
            try:
                message = queue.get(timeout=0.1)
                if message:
                    message_obj = json.dumps(message)
                    self.consumer_object.publish_message(message_obj)
                    logging.info(f"##### Consumed and published message #####\n")
                else:
                    logging.info(f"##### Hit sentinel stopping consumer #####\n")
                    break

            except Empty:
                continue

            
