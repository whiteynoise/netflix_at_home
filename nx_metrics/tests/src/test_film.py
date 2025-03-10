from unittest.mock import patch

import requests

BASE_URL = "http://test_api:5000"


@patch("producer.KafkaProducer")
def test_user_event_valid(mock_send_to_kafka):
    from app import app

    client = app.test_client()
    payload = {
        "film_event_tag": "watch",
        "film_id": "1",
    }
    response = client.post("film_event/", json=payload)
    assert response.status_code == 200
    res_json = response.get_json()
    assert res_json["user_id"] == "2e991ac8-a0d5-46bf-973a-ee65199e06f0"
    assert res_json["film_event_tag"] == "watch"
    assert res_json["film_id"] == "1"


@patch("core.film.send_to_kafka")
def test_user_event_invalid(mock_send_to_kafka):
    from app import app

    client = app.test_client()
    payload = {"user_event_tag": None}
    response = client.post("film_event/", json=payload)
    assert response.status_code == 400
