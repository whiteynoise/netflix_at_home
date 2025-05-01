from enum import Enum

BLACKLIST = "blacklist"


class RoleName(str, Enum):
    ADMIN = "admin"
    BASE_USER = "base_user"
    SUB_USER = "sub_user"


TEMPLATE_ID = "4e8c3f34-a70d-41ff-8b4d-4bb22aeaf14e"
SINGLE_NOTIFICATION_SERVICE_API = (
    "http://single_notification_api:8888/api/v1/create_notification"
)
