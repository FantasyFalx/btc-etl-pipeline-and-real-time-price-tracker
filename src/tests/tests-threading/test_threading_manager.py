# Standard libraries
import threading
import time

# 3rd party
import pytest

# Custom modules
# from constants import


    
# I am going to need to model a message call for the producer test. 
# Seems like this calls for a fixture. 


def test_producer(thread_manager_factory, producer_callable, consumer_callable):
    manager = thread_manager_factory(producer_callable, consumer_callable)
    
    # Configs
    event = threading.Event()
    message_queue = manager.message_queue
    
    # Start producer in a thread
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
    
    #assert not producer_thread.is_alive()


## TODO: Add tests for consumer and execute_threads later.
#def test_consumer(thread_manager_factory):
#    manager = thread_manager_factory
#    pass
#
#
#def test_execute_threads(thread_manager_factory):
#    manager = thread_manager_factory
#    pass
