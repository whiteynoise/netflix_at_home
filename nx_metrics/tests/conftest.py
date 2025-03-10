import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def mock_kafka_producer():
    with patch("kafka.KafkaProducer") as mock_producer:
        mock_instance = MagicMock()
        mock_producer.return_value = mock_instance
        yield mock_instance
