"""Pytest fixtures for Apache Beam Dataflow pipeline module tests."""

## IMPORTS ##
# STANDARD LIBRARIES
# 3RD PARTY LIBRARIES
import pytest
import json

# CUSTOM IMPORTS
from beam_constants import (
    MOCK_MESSAGE,
)

##############

# TODO: Determine how to change the object types. ##
@pytest.fixture
def bytes_mock_message():
    mock_message = json.dumps(MOCK_MESSAGE)
    return mock_message.encode('utf-8')

@pytest.fixture
def encoded_mock_message():
    return json.dumps(MOCK_MESSAGE)


if __name__ == "__main__":
    None
else:
    None
