import random
import string

from mixer.backend.django import mixer
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class DRFClient(APIClient):
    def __init__(self, user=None, god_mode=True, anon=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not anon:
            self.auth(user, god_mode)

    def auth(self, user=None, god_mode=True):
        self.user = user or self._create_user(god_mode)
        self.god_mode = god_mode

        token = Token.objects.create(user=self.user)
        self.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def _create_user(self, god_mode=True):
        user_opts = dict()
        if god_mode:
            user_opts = {
                "is_staff": True,
                "is_superuser": True,
            }
        user = mixer.blend("users.User", **user_opts)
        self.password = "".join([random.choice(string.hexdigits) for _ in range(0, 6)])
        user.set_password(self.password)
        user.save()
        return user

    def logout(self):
        self.credentials()
        super().logout()
