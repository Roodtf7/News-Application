"""
Application configuration for the articles application.
Defines the metadata and initialization logic for the articles management component.
"""
from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    """
    Configuration for the articles app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = 'articles'
