"""Pub/Sub publisher module for streaming BTC price messages to GCP."""

## IMPORTS ##
# STANDARD LIBRARIES
# 3RD PARTY LIBRARIES
from google.cloud import pubsub_v1
#from google.cloud import secretmanager
#from google.oauth2 import service_account
from googleapiclient.errors import HttpError
# CUSTOM IMPORTS
##############



class PubSubPublisher:
    """Publishes validated messages to a GCP Pub/Sub topic."""

    def __init__(self) -> None:
        self._publisher_client: pubsub_v1.PublisherClient | None = None

    def set_publisher_client(self, publisher_client: pubsub_v1.PublisherClient) -> None:
        self._publisher_client = publisher_client

    def get_publisher_client(self) -> pubsub_v1.PublisherClient | None:
        return self._publisher_client


if __name__ == "__main__":
    client = pubsub_v1.PublisherClient()
    print("it worked!!!")
else:
    None
