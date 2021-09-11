from datetime import date

import pytest

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(
    "due_date, expected",
    (
        (date(2032, 3, 1), True),
        (date(2032, 3, 2), False),
        (date(2032, 3, 3), False),
    ),
)
def test_subscription_is_stale(subscription, freezer, due_date, expected):
    freezer.move_to("2032-03-02")
    subscription.due_date = due_date
    subscription.save()

    assert subscription.is_stale() is expected
