from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property


class UserQuerySet(models.QuerySet):
    def for_viewset(self):
        return self


class CustomUserManager(UserManager.from_queryset(UserQuerySet)):
    pass


class User(AbstractUser):
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        is_new = not self.pk

        super().save(*args, **kwargs)

        if is_new:
            Subscription = apps.get_model("bookstore.Subscription")
            Subscription.objects.create(
                user=self,
                due_date=timezone.now().date()
                + settings.USER_BOOKSTORE_TRIAL_PERIOD_ON_CREATION,
            )

    @cached_property
    def full_name(self):
        return self.get_full_name()
