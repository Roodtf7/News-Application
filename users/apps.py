"""
Application configuration for the users application.
Initializes custom user management and ensures authentication signals are correctly registered.
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration for the users app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = 'users'

    def ready(self):
        """
        Connect signals for the users app.
        """
        import users.signals
