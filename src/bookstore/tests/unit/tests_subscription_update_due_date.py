from datetime import date, timedelta

import pytest

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(
    "old_due_date, expected",
    (
        (date(2032, 2, 1), date(2032, 3, 12)),  # if subscription is stale - add to now
        (
            date(2032, 3, 2),
            date(2032, 3, 12),
        ),  # if subscription is not stale - add to due_date
        (date(2032, 3, 3), date(2032, 3, 13)),
    ),
)
def test_subscription_is_stale(subscription, freezer, old_due_date, expected):
    freezer.move_to("2032-03-02")
    subscription.due_date = old_due_date
    subscription.save()

    subscription.update_due_date_after_payment(timedelta(days=10))
    subscription.refresh_from_db()

    assert subscription.due_date == expected
