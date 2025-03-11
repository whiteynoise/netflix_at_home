from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from schema import FilmEventSchema
from utils import send_to_kafka

film_bp = Blueprint("/film_event", __name__, url_prefix="/film_event")


@film_bp.route("/", methods=["POST"])
def film_event() -> tuple:
    schema = FilmEventSchema()
    try:
        json_data = request.get_json()
        validated_data = schema.load(json_data)
        send_to_kafka(topic="film", message=validated_data)
        return jsonify(validated_data), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
