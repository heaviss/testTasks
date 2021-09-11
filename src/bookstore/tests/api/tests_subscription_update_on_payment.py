from datetime import date

import pytest

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def subscription(subscription):
    subscription.due_date = date(2032, 3, 1)
    subscription.save()
    return subscription


@pytest.fixture
def post_data(user):
    return {"user_id": f"{user.pk}", "status": "ok", "period": "year"}


def test_forbidden_for_anon(anon_api, user, post_data):
    got = anon_api.post("/api/v1/add_user_payment/", post_data)

    assert got.status_code == 401


def test_forbidden_for_non_admin(api, user, post_data):
    got = api.post("/api/v1/add_user_payment/")

    assert got.status_code == 403


def test_updates_subscription(admin_api, subscription, book, post_data):
    got = admin_api.post("/api/v1/add_user_payment/", post_data).json()

    subscription.refresh_from_db()

    assert got == "ok"
    assert subscription.due_date == date(2033, 3, 2)


@pytest.mark.parametrize(
    "break_data",
    (
        lambda data: data.update({"status": "fuck you"}),
        lambda data: data.update({"period": "century"}),
        lambda data: data.update({"user_id": "13.37"}),
    ),
)
def test_400_on_bad_data(admin_api, subscription, post_data, break_data):
    break_data(post_data)

    got = admin_api.post("/api/v1/add_user_payment/", post_data)

    assert got.status_code == 400
