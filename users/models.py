"""
Models for the users application.
Defines the custom User model with integrated role-based access control and profile management.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model used for the News Application.
    Supports role-based access such as reader, journalist, and editor.
    """
    ROLE_CHOICES = (
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="reader",
    )

    is_reader = models.BooleanField(default=False)
    is_journalist = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)

    @property
    def registered_roles(self):
        """
        Return a list of roles the user is registered as.
        """
        roles = []
        if self.is_reader: roles.append("reader")
        if self.is_journalist: roles.append("journalist")
        if self.is_editor: roles.append("editor")
        return roles


    def __str__(self):
        """
        Return the string representation of the user.
        """
        return f"{self.username} ({self.role})"

    @property
    def reader_subscriptions(self):
        """
        Returns subscriptions if the user is a reader, else None.
        """
        if self.role == "reader":
            return self.subscriptions.all()
        return None

    @property
    def journalist_articles(self):
        """
        Returns authored articles if the user is a journalist, else None.
        """
        if self.role == "journalist":
            return self.articles.all()
        return None

    @property
    def journalist_newsletters(self):
        """
        Returns authored newsletters if the user is a journalist, else None.
        """
        if self.role == "journalist":
            return self.newsletters.all()
        return None
