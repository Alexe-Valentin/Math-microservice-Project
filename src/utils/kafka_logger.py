import json
from kafka import errors
from kafka import KafkaProducer


class KafkaLogger:
    def __init__(self, bootstrap_servers, client_id=None):
        # Don’t create producer here—just remember the settings
        self.bootstrap_servers = bootstrap_servers
        self.client_id = client_id
        self._producer = None

    def _ensure_producer(self):
        # Create the producer on first use
        if self._producer is None:
            try:
                self._producer = KafkaProducer(
                    bootstrap_servers=self.bootstrap_servers,
                    client_id=self.client_id,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                )
            except errors.NoBrokersAvailable:
                # No Kafka broker reachable—disable Kafka for this run
                self._producer = None

    def send(self, topic: str, message: dict):
        # Lazily initialize the producer
        self._ensure_producer()
        if not self._producer:
            return  # no-op if we failed to connect
        # Otherwise send normally
        self._producer.send(topic, value=message)
        self._producer.flush()
