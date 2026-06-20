# Standard libraries
import threading
import time

# 3rd party

# Custom modules
from threading_constants import VALID_YFINANCE_BTC_MESSAGE, INVALID_YFINANCE_BTC_MESSAGE

def test_producer(
    thread_manager_factory, yfinance_manager_factory, pubsub_publisher_factory
):
    manager = thread_manager_factory(
        yfinance_manager_factory, pubsub_publisher_factory
    )
    
    # Configs
    event = threading.Event()
    message_queue = manager.message_queue

    for message in range(4):
        message_queue.put(f"message_{message}")
    
    # Start producer in a thread
    # Inserts items into the thread. 
    producer_thread = threading.Thread(
        target=manager.producer, args=(message_queue, event)
    )
    producer_thread.start()
    # Let the producer run for a short whiles
    time.sleep(1)
    # Signal the producer to stop
    event.set()
    # Get item from the queue, so it does not hang. 
    """
    This is so the test does not fail and hang when queue fills. 
    The queue fills fast, and on the next put it hangs because it hits the maxsize. 
    You need to remove one item from the queue to allow the next put to succeed
    so the loop does not hang. 
    ** Refactor this explanation later **. 
    """
    message_queue.get()
    producer_thread.join(timeout=2)

    # Check if at least one item is in the queue and thread is not alive
    assert message_queue.qsize() > 0 and not producer_thread.is_alive() # Adjust as per what producer actually does
    

def test_consumer(thread_manager_factory, producer_callable, pubsub_publisher_factory):
    manager = thread_manager_factory(producer_callable, pubsub_publisher_factory) 
    event = threading.Event()
    queue = manager.message_queue
    sample_size = 10

    for msg in range(sample_size):
        queue.put(f"msg_{msg}")

    event.set()
    manager.consumer(queue, event)
    assert queue.qsize() == 0



def test_execute_threads(
    thread_manager_factory, yfinance_manager_factory, pubsub_publisher_factory
):
    manager = thread_manager_factory(yfinance_manager_factory, pubsub_publisher_factory)
    manager.execute_threads()
    manager.event.set()
    assert manager.message_queue.qsize() == 0 and manager.event.is_set()


def test_queue_gluer_puts_valid_message(
    thread_manager_factory, yfinance_manager_factory, pubsub_publisher_factory
):
    manager = thread_manager_factory(yfinance_manager_factory, pubsub_publisher_factory)
    manager.queue_gluer(VALID_YFINANCE_BTC_MESSAGE)
    assert manager.message_queue.get() == VALID_YFINANCE_BTC_MESSAGE


def test_queue_gluer_skips_invalid_message(
    thread_manager_factory, yfinance_manager_factory, pubsub_publisher_factory
):
    manager = thread_manager_factory(yfinance_manager_factory, pubsub_publisher_factory)
    manager.queue_gluer(INVALID_YFINANCE_BTC_MESSAGE)
    assert manager.message_queue.qsize() == 0
