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
 

class ThreadManager:
    def __init__(self, queue: Queue):
        self.thread: threading.Thread | None = None
        self.thread_running: bool = False
        # Message queue should live in the thread manager or the finance manager? 
        # I have to decide on this? 
        self.message_queue: Queue = queue

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

    def execute_thread(self, ) -> None:
        # Main method to execute the workflow. 
        # Set two exectuors in a thread pool with the context manager. 
            # Run the producer 
            # Run the consumer

        # Determine a condition to set the event. 
        # A solid condition for the event to be set
        

        return None    

    def producer(self, message_queue: Queue, event: threading.Event) -> None:
        # This will be for the yfinance manager. 
        # Create the yahoo finance manager. 
        # Run the web socket. 
        return None

    def consumer(self, message_queue: Queue, event: threading.Event) -> None:
        # This will be for the pub/sub topic. 
        # Keep consumer one while the event is not set or queue is not empty. 
            # Pop the message from the queue. 
            # Push the messasge and send to the pub/sub topic. 
        return None


    

    
   