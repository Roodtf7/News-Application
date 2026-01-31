"""
ASGI config for news_project project.
It exposes the ASGI callable as a module-level variable named ``application``.
Encapsulates the asynchronous entry point for the application, supporting real-time capabilities.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')

application = get_asgi_application()
