"""
Application configuration for the notifications application.
Handles the registration of signals to automate notifications upon article approval.
"""
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """
    Configuration for the notifications app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = 'notifications'

    def ready(self):
        """
        Connect signals for the notifications app.
        """
        import notifications.signals