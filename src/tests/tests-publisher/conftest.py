"""Pytest fixtures for PubSubPublisher module tests."""

## IMPORTS ##
# STANDARD LIBRARIES
# 3RD PARTY LIBRARIES
import pytest
# Custom modules
from btc_streaming_etl.pubsub.pubsub_publisher import PubSubPublisher
from googleapiclient.errors import HttpError
from constants import MOCK_PATHS, MOCK_TOPIC_PATH
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

@pytest.fixture
def mock_http_error(
    mocker, publisher_factory_fixture
):
    # TAkes 3 gives 4? 
    mocker.patch(
        MOCK_PATHS["set_publisher_client"], 
        side_effect = HttpError(
            # Status code, reason, content, uri
            # It needs a resonse object insted of an int.  
            resp=mocker.MagicMock(status=400, reason="Bad Request"),
            content=b"Bad Request",
            uri="https://failed-to-set-publisher-client.com"
        )
    )
    return publisher_factory_fixture
    
@pytest.fixture
def mock_pub_sub_topic_path(
    mocker, publisher_factory_fixture
):
    client = mocker.MagicMock()
    client.topic_path.return_value = MOCK_TOPIC_PATH
    publisher_factory_fixture._publisher_client = client

    return publisher_factory_fixture

"""
client = mocker.MagicMock()
    client.topic_path.return_value = MOCK_TOPIC_PATH
    publisher_factory_fixture._publisher_client = client

    return publisher_factory_fixture


"""

if __name__ == "__main__":
    None
else:
    None
