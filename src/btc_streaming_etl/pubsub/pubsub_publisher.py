"""Pub/Sub publisher module for streaming BTC price messages to GCP."""

## IMPORTS ##
# STANDARD LIBRARIES
import logging
import json
# 3RD PARTY LIBRARIES
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import pubsub_v1
# CUSTOM IMPORTS
##############


class PubSubPublisher:
    """Publishes validated messages to a GCP Pub/Sub topic."""

    def __init__(self) -> None:
        self._publisher_client: pubsub_v1.PublisherClient | None = None
        self._topic_path: str | None = None
        self.TOPIC_ID: str = "btc_price_topic"
        self.PROJECT_ID: str = "bitcoin-streaming-etl-project"

    def publish_message(self, message: str) -> None:
        try:
            data = message.encode("utf-8")
            future = self._publisher_client.publish(self._topic_path, data)
            return future.result()
        except GoogleAPICallError as e:
            logging.error("Error publishing message: %s.", e)
            raise e
    
    def set_topic_path(self) -> None:
        try:
            logging.info("Setting topic path.")
            self._topic_path = self._publisher_client.topic_path(
                self.PROJECT_ID,
                self.TOPIC_ID,
            )
            logging.info("Topic path set successfully.")
        except GoogleAPICallError as e:
            logging.error("Error setting topic path: %s.", e)
            raise e

    def set_publisher_client(self) -> None:
        try: 
            logging.info("Setting publisher client.")
            self._publisher_client = pubsub_v1.PublisherClient()
            logging.info("Publisher client set successfully.")
        except GoogleAPICallError as e:
            logging.error("Error setting publisher client: %s.", e)
            raise e


if __name__ == "__main__":
   None
else:
    None
