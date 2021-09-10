import pytest
from django.test import override_settings as django_override_settings
from mixer.backend.django import mixer as _mixer

from _app.test.api_client import DRFClient


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def user(mixer):
    return mixer.blend("users.User", password="123")


@pytest.fixture
def api(user) -> DRFClient:
    client = DRFClient(user=user)
    return client


@pytest.fixture
def anon_api(api) -> DRFClient:
    api.logout()
    return api


@pytest.fixture
def admin_api(api, user) -> DRFClient:
    user.is_staff = True
    user.is_superuser = True
    user.save()

    return api


@pytest.fixture
def override_settings():
    return django_override_settings
