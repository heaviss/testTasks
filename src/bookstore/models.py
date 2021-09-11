from datetime import timedelta

from django.db import models
from django.utils import timezone


class SubscriptionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(due_date__gte=timezone.now().date())


class Subscription(models.Model):
    objects = SubscriptionQuerySet.as_manager()

    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="subscription"
    )

    due_date = models.DateField()

    def update_due_date_after_payment(self, payment_period: timedelta):
        if not payment_period:
            return

        if self.is_stale():
            self.due_date = timezone.now() + payment_period
        else:
            self.due_date = self.due_date + payment_period

        self.save()

    def is_stale(self):
        return self.due_date < timezone.now().date()


class Book(models.Model):
    name = models.CharField(max_length=256)
