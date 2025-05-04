import enum

TEMPLATE_PATH = "templates/"


class VolumeEventType(str, enum.Enum):
    SINGLE = "single"
    MASSIVE = "massive"


class TimeEventType(str, enum.Enum):
    INSTANT = "instant"
    DEFERRED = "deferred"


class NotificationEventType(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"


SINGLE_NOTIFICATION_SERVICE_API = "http://single_notification_api:8888/api/v1/create_notification"
MASSIVE_NOTIFICATION_SERVICE_API = "http://massive_notification_api:8889/api/v1/create_notification"
SCHEDULER_URL = "http://scheduler_events:8887/create_deferred_event"
