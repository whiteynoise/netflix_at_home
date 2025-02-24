from datetime import datetime

import jwt
from flask import request
from marshmallow import fields, Schema, pre_load, ValidationError

from constants import SECRET_KEY, ALGORITHM


class EventSchema(Schema):
    type = fields.Str()
    tag = fields.Str(allow_none=True)
    user_id = fields.UUID(allow_none=True, required=False)
    event_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', default=datetime.utcnow)

    @pre_load
    def extract_user_id(self, data, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            data['user_id'] = None
            return data
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            data['user_id'] = payload.get('user_id')
        except jwt.ExpiredSignatureError:
            raise ValidationError('Token expired')
        except jwt.InvalidTokenError:
            raise ValidationError('Invalid token')
        return data


class UserEventSchema(EventSchema):
    pass


class FilmEventSchema(EventSchema):
    film_id = fields.UUID()
