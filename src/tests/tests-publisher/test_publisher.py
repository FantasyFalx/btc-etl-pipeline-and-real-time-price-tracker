"""Unit tests for the PubSubPublisher module."""

## IMPORTS ##
# STANDARD LIBRARIES
# 3RD PARTY LIBRARIES
import pytest
from googleapiclient.errors import HttpError
# CUSTOM IMPORTS
from constants import MOCK_TOPIC_PATH
##############

## Set client method ##
def test_set_publisher_client_success(publisher_factory_fixture):
    publisher = publisher_factory_fixture
    publisher.set_publisher_client()
    assert publisher._publisher_client is not None

def test_set_publisher_client_failure(mock_http_error):
    publisher = mock_http_error
    with pytest.raises(HttpError):
        publisher.set_publisher_client()

def test_set_topic_path_success(mock_pub_sub_topic_path):
    publisher = mock_pub_sub_topic_path
    publisher.set_topic_path()
    assert publisher._topic_path == MOCK_TOPIC_PATH
    
if __name__ == "__main__":
    None
else:
    None


