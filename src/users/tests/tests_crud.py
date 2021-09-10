import pytest

from users.models import User

pytestmark = [
    pytest.mark.django_db,
]


def test_list_forbidden_for_anon(anon_api, user):
    got = anon_api.get("/api/v1/users/")

    assert got.status_code == 401


def test_list_forbidden_for_non_admin_users(api, user):
    got = api.get("/api/v1/users/")

    assert got.status_code == 403


def test_list(admin_api, user):
    got = admin_api.get("/api/v1/users/").json()

    assert len(got) == 1
    assert got[0]["id"] == user.id
    assert got[0]["username"] == user.username
    assert got[0]["full_name"] == user.full_name


def test_retrieve(admin_api, user):
    got = admin_api.get(f"/api/v1/users/{user.pk}/").json()

    assert got["id"] == user.id
    assert got["username"] == user.username
    assert got["full_name"] == user.full_name


def test_create(admin_api, user):
    got = admin_api.post("/api/v1/users/", {"username": "johndoe"}).json()

    created_user = User.objects.latest("id")

    assert got["id"] == created_user.id
    assert got["username"] == "johndoe"
