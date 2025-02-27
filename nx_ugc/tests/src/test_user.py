from unittest.mock import patch

import requests


@patch("core.user.send_to_kafka")
def test_user_event_valid(mock_send_to_kafka):
    from app import app
    client = app.test_client()
    payload = {"user_event_tag": "login"}
    response = client.post("user_event/", json=payload)
    assert response.status_code == 200
    res_json = response.get_json()
    assert res_json["user_id"] == "2e991ac8-a0d5-46bf-973a-ee65199e06f0"
    assert res_json["user_event_tag"] == "login"


@patch("core.user.send_to_kafka")
def test_user_event_invalid(mock_send_to_kafka):
    from app import app
    client = app.test_client()
    payload = {"user_event_tag": None}
    response = client.post("user_event/", json=payload)
    assert response.status_code == 400
