"""
Models for the subscriptions application.
Defines the Subscription entity which links Readers to their favorite Publishers or Journalists.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from publishers.models import Publisher

User = settings.AUTH_USER_MODEL


class Subscription(models.Model):
    """
    Represents a reader's subscription to a publisher or journalist.
    Used to determine who receives notifications when articles are published.
    """
    reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    publisher = models.ForeignKey(
        Publisher,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    journalist = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subscribed_journalists",
    )

    def clean(self):
        """
        Validate that a subscription is either to a publisher or a journalist, but not both or none.
        """
        if bool(self.publisher) == bool(self.journalist):
            raise ValidationError(
                "Subscription must be to either a publisher or a journalist."
            )

    def __str__(self):
        """
        Return the string representation of the subscription.
        """
        target = self.publisher or self.journalist
        return f"{self.reader} → {target}"
