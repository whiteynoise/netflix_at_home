import json

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from config import settings

CustomUser = get_user_model()


class AuthBackend(BaseBackend):
    """Бекенд для логина в сервисе аунтификации. Подойдет и обычный юзер"""

    def authenticate(self, request, username=None, email=None, password=None):
        auth_api = settings.AUTH_API
        payload = {"username": username, "email": email, "password": password}
        response = requests.post(auth_api, data=json.dumps(payload))

        if response.status_code != 200:
            return

        data = response.json()

        try:
            user, created = CustomUser.objects.get_or_create(id=data["user_id"])
            user.email = data.get("email")
            user.username = data.get("username")
            user.first_name = data.get("first_name")
            user.last_name = data.get("last_name")
            user.is_staff = data.get("is_stuff")
            user.is_admin = "admin" in data.get("roles")
            user.is_superuser = data.get("is_superuser")
            user.is_active = data.get("is_active")
            user.save()
        except Exception as e:
            return

        return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return
