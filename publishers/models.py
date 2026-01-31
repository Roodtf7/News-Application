"""
Models for the publishers application.
Defines the Publisher organization model and its relationships with Editors and Journalists.
"""
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Publisher(models.Model):
    """
    Represents a news publisher that groups journalists and articles
    under a single organization.
    """
    name = models.CharField(max_length=255, unique=True)

    editors = models.ManyToManyField(
        User,
        related_name="editor_publishers",
        blank=True,
    )

    journalists = models.ManyToManyField(
        User,
        related_name="journalist_publishers",
        blank=True,
    )

    def __str__(self):
        """
        Return the string representation of the publisher.
        """
        return self.name
