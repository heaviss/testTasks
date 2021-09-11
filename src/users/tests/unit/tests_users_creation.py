from datetime import date

import pytest

pytestmark = [
    pytest.mark.django_db,
]


def test_create_subscription_for_user_on_creation(mixer, freezer):
    freezer.move_to("2032-03-02")

    user = mixer.blend("users.User")

    assert user.subscription.due_date == date(2032, 3, 2 + 14)
