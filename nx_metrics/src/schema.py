import time

from flask import request
from marshmallow import Schema, fields, pre_load


class UserEventSchema(Schema):
    user_event_tag = fields.Str()
    user_id = fields.Str(allow_none=True, required=False)
    event_time = fields.Str(required=False)

    @pre_load
    def extract_user_id(self, data, **kwargs):
        token = request.headers.get("Authorization")
        data["event_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        if not token:
            data["user_id"] = "2e991ac8-a0d5-46bf-973a-ee65199e06f0"
            return data
        return data


class FilmEventSchema(Schema):
    film_event_tag = fields.Str(allow_none=True)
    film_id = fields.Str()
    user_id = fields.Str(allow_none=True, required=False)
    event_time = fields.Str(required=False)

    @pre_load
    def extract_user_id(self, data, **kwargs):
        token = request.headers.get("Authorization")
        data["event_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        if not token:
            data["user_id"] = "2e991ac8-a0d5-46bf-973a-ee65199e06f0"
            return data
        return data
