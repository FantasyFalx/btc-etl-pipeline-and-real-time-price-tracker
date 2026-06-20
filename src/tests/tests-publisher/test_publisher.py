"""Unit tests for the PubSubPublisher module."""

## IMPORTS ##
# STANDARD LIBRARIES
# 3RD PARTY LIBRARIES
import pytest
from google.api_core.exceptions import GoogleAPICallError
# CUSTOM IMPORTS
from publisher_constants import MOCK_TOPIC_PATH, MOCK_MESSAGE, RESULT_STRING
##############

## Set client method ##
def test_set_publisher_client_success(publisher_factory_fixture):
    publisher = publisher_factory_fixture
    publisher.set_publisher_client()
    assert publisher._publisher_client is not None

def test_set_publisher_client_failure(mock_google_api_error):
    publisher = mock_google_api_error
    with pytest.raises(GoogleAPICallError):
        publisher.set_publisher_client()

def test_set_topic_path_success(mock_pub_sub_topic_path):
    publisher = mock_pub_sub_topic_path
    publisher.set_topic_path()
    assert publisher._topic_path == MOCK_TOPIC_PATH


def test_set_topic_path_failure(mock_google_api_error):
    publisher = mock_google_api_error
    with pytest.raises(GoogleAPICallError):
        publisher.set_topic_path()

def test_publish_message_success(mock_publish_message_success):
    publisher = mock_publish_message_success
    result = publisher.publish_message(MOCK_MESSAGE)
    assert result == RESULT_STRING

def test_publish_message_failure(mock_google_api_error):
    publisher = mock_google_api_error
    with pytest.raises(GoogleAPICallError):
        publisher.publish_message(MOCK_MESSAGE)


if __name__ == "__main__":
    None
else:
    None


