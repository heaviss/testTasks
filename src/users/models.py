from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.functional import cached_property


class UserQuerySet(models.QuerySet):
    def for_viewset(self):
        return self


class CustomUserManager(UserManager.from_queryset(UserQuerySet)):
    pass


class User(AbstractUser):
    # todo: add 2 week trial period on creation
    objects = CustomUserManager()

    @cached_property
    def full_name(self):
        return self.get_full_name()
