from enum import Enum

BLACKLIST = 'blacklist'


class RoleName(str, Enum):
    ADMIN = 'admin'
    BASE_USER = 'base_user'
    SUB_USER = 'sub_user'
