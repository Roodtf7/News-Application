"""
URL routing for the subscriptions application.
Defines paths for users to manage their content subscriptions and newsletters.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("subscriptions/", views.subscription_list, name="subscription-list"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("unsubscribe/<int:subscription_id>/", views.unsubscribe, name="unsubscribe"),
]
