TEMPLATE_PATH = "templates/"

import enum


class EventType(enum.Enum):
    REGULAR = "regular"
    INSTANCE = "instance"


INSTANCE_NOTIFICATION_SERVICE_API = "http://instance_notification_api:8888/api/v1/create_notification"
REGULAR_NOTIFICATION_SERVICE_API = "http://regular_notification_api:8889/api/v1/create_notification"
