from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError

from schema import UserEventSchema, FilmEventSchema
from utils import send_to_kafka

app = Flask(__name__)
ma = Marshmallow(app)


@app.route('/ping')
def health():
    return 'Pong', 200


@app.route('/film_event', methods=["POST"])
def film_event():
    schema = FilmEventSchema()
    try:
        json_data = request.get_json()
        validated_data = schema.load(json_data)
        send_to_kafka(topic="film", message=validated_data)
        return jsonify(validated_data), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


@app.route('/user_event', methods=["POST"])
def user_event():
    schema = UserEventSchema()
    try:
        json_data = request.get_json()
        validated_data = schema.load(json_data)
        send_to_kafka(topic="user", message=validated_data)
        return jsonify(validated_data), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


if __name__ == '__main__':
    app.run()
