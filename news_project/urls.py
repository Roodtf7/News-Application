"""
Root URL configuration for the news_project.
Defines the top-level paths and orchestrates routing between user, article, and API apps.
Provides the entry point for all web requests to the news application.
"""
from django.contrib import admin
from django.urls import path, include
from users.views import landing_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing_page, name="landing-page"),
    path("", include("articles.urls")),
    path("", include("publishers.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("api/", include("api.urls")),
    path("", include("subscriptions.urls")),
]
