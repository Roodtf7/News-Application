"""
URL routing for the API application.
Maps API endpoints to their corresponding view classes for resource retrieval.
"""
from django.urls import path
from .views import SubscribedArticlesView


urlpatterns = [
    path("articles/", SubscribedArticlesView.as_view(), name="subscribed-articles"),
]
