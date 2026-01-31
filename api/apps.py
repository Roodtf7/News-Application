"""
Application configuration for the API application.
Defines the metadata and lifecycle hooks for the API component of the news project.
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Configuration for the api app.
    """
    name = 'api'
