from datetime import date

import pytest

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def book(mixer):
    return mixer.blend("bookstore.Book")


def test_list_forbidden_for_anon(anon_api, user):
    got = anon_api.get("/api/v1/books/")

    assert got.status_code == 401


def test_list(api, user, book):
    got = api.get("/api/v1/books/").json()

    assert len(got) == 1
    assert got[0]["id"] == book.id
    assert got[0]["name"] == book.name


def test_retrieve(api, user, book):
    got = api.get(f"/api/v1/books/{book.pk}/").json()

    assert got["id"] == book.id
    assert got["name"] == book.name


def test_retrieve_forbidden_if_user_subscription_is_stale(api, freezer, user, book):
    freezer.move_to("2032-03-02")
    user.subscription.due_date = date(2032, 3, 1)
    user.subscription.save()

    got = api.get(f"/api/v1/books/{book.pk}/")

    assert got.status_code == 403
