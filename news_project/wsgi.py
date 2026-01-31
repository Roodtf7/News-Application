"""
WSGI config for news_project project.
It exposes the WSGI callable as a module-level variable named ``application``.
Provides the synchronous interface between the web server and the Django application.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')

application = get_wsgi_application()
