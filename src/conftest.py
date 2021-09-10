import pytest
from django.test import override_settings as django_override_settings
from mixer.backend.django import mixer as _mixer
from rest_framework.test import APIClient


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def api() -> APIClient:
    return APIClient()


# @pytest.fixture
# def anon_api() -> APIClient:
#     return APIClient(anon=True)


@pytest.fixture
def override_settings():
    return django_override_settings
