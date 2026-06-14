"""Pytest fixtures for PubSubPublisher module tests."""

## IMPORTS ##
# STANDARD LIBRARIES
# 3RD PARTY LIBRARIES
import pytest
# Custom modules
from btc_streaming_etl.pubsub.pubsub_publisher import PubSubPublisher
from constants import MOCK_PUBLISHER_CLIENT_PATH
# CUSTOM IMPORTS
##############


## Fixtures ##
@pytest.fixture
def publisher_factory_fixture(mocker):
    mocker.patch(
        MOCK_PUBLISHER_CLIENT_PATH,
        return_value=mocker.MagicMock()
    )

    return PubSubPublisher()

if __name__ == "__main__":
    None
else:
    None
