# IMPORT STANDARD LIBRARIES
import threading
from queue import Queue
import logging

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
    def __init__(self, producer_object, consumer_object):
        self.thread: threading.Thread | None = None
        self.thread_running: bool = False
        self.message_queue: Queue = Queue(maxsize=1000)
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

    # The producer will be itss ''

    """
     Having this module manage threading for pub/sub and yfinance manager 
     is logical because it separates the concerns of threading from the 
     pub/sub and yfinance manager.
     While this just holds the shared resource between the two. I won't need to 
     input
    
    """

    def execute_threads(self) -> None:
        # Main method to execute the workflow. 
        # Set two exectuors in a thread pool with the context manager. 
            # Run the producer 
            # Run the consumer

        # Determine a condition to set the event. 
        # A solid condition for the event to be set
        return None    

    def producer(self, queue: Queue, event: threading.Event) -> None:
        while not event.is_set():
            message = self.producer_object()
            print(f"Producer message: {message}")
            queue.put(message)
            print(f"Size of queue: {queue.qsize()}")
   

    def consumer(self, message_queue: Queue, event: threading.Event) -> None:
        # This will be for the pub/sub topic. 
        # Keep consumer one while the event is not set or queue is not empty. 
            # Pop the message from the queue. 
            # Push the messasge and send to the pub/sub topic. 
        return None


    

    
   