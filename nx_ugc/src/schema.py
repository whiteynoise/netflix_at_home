import time

from flask import request
from marshmallow import fields, Schema, pre_load, ValidationError

from constants import SECRET_KEY, ALGORITHM


class EventSchema(Schema):
    user_id = fields.Str(allow_none=True, required=False)
    event_time = fields.Str(required=False)

    @pre_load
    def extract_user_id(self, data, **kwargs):
        token = request.headers.get('Authorization')
        data["event_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        if not token:
            data['user_id'] = "2e991ac8-a0d5-46bf-973a-ee65199e06f0"
            return data
        # try:
        #     payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        #     data['user_id'] = payload.get('user_id')
        # except InvalidSignatureError:
        #     raise ValidationError('Token expired')
        # except PyJWTError:
        #     raise ValidationError('Invalid token')
        return data


class UserEventSchema(EventSchema):
    user_event_tag = fields.Str(allow_none=True)


class FilmEventSchema(EventSchema):
    film_event_tag = fields.Str(allow_none=True)
    film_id = fields.Str()
