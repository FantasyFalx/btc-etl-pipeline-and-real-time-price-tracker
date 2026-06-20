"""Pytest fixtures for PubSubPublisher module tests."""

## IMPORTS ##
# STANDARD LIBRARIES
# 3RD PARTY LIBRARIES
import pytest
# Custom modules
from btc_streaming_etl.pubsub.pubsub_publisher import PubSubPublisher
from google.api_core.exceptions import GoogleAPICallError
from publisher_constants import (
    MOCK_PATHS, 
    MOCK_TOPIC_PATH, 
    RESULT_STRING, 
)
# CUSTOM IMPORTS
##############


## Fixtures ##
@pytest.fixture
def publisher_factory_fixture(mocker):
    mocker.patch(
        MOCK_PATHS["set_publisher_client"],
        return_value=mocker.MagicMock()
    )

    return PubSubPublisher()

def google_api_error_patch_returner(mocker, path):
    return mocker.patch(
        path, side_effect = GoogleAPICallError(
            "Bad Request",
        )
    )

@pytest.fixture
def mock_google_api_error(
    mocker, publisher_factory_fixture
):
    
    for path in MOCK_PATHS:
        google_api_error_patch_returner(mocker, MOCK_PATHS[path])
    
    return publisher_factory_fixture
    
@pytest.fixture
def mock_pub_sub_topic_path(
    mocker, publisher_factory_fixture
):
    client = mocker.MagicMock()
    client.topic_path.return_value = MOCK_TOPIC_PATH
    publisher_factory_fixture._publisher_client = client

    return publisher_factory_fixture


@pytest.fixture
def mock_publish_message(
    mocker, publisher_factory_fixture
):
    mocker.patch(
        MOCK_PATHS["publish_message"],
        return_value=mocker.MagicMock()
    )
    return publisher_factory_fixture

@pytest.fixture
def mock_publish_message_success(mocker, publisher_factory_fixture):
    mocker.patch(
        MOCK_PATHS["publish_message"],
        return_value=mocker.MagicMock()
    )
    client = mocker.MagicMock() 
    publisher_factory_fixture._publisher_client = client
    publisher_factory_fixture.publish_message.return_value = RESULT_STRING
    return publisher_factory_fixture


if __name__ == "__main__":
    None
else:
    None
