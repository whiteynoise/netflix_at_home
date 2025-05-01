import enum


class VolumeEventType(str, enum.Enum):
    single = "single"
    massive = "massive"

