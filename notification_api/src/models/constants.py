import enum


class VolumeEventType(str, enum.Enum):
    single = "single"
    massive = "massive"


class NotificationEventType(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
