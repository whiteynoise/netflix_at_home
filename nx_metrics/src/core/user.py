from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from schema import UserEventSchema
from utils import send_to_kafka

user_bp = Blueprint("/user_event", __name__, url_prefix="/user_event")


@user_bp.route("/", methods=["POST"])
def user_event():
    schema = UserEventSchema()
    try:
        json_data = request.get_json()
        validated_data = schema.load(json_data)
        send_to_kafka(topic="user", message=validated_data)
        return jsonify(validated_data), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
