import pytest


@pytest.fixture
def book(mixer):
    return mixer.blend("bookstore.Book")


@pytest.fixture
def subscription(user):
    return user.subscription
