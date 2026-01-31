"""
Admin configuration for the subscriptions application.
Provides management of reader subscriptions to publishers and journalists.
"""
from django.contrib import admin
from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Subscription model.
    """
    list_display = ("reader", "publisher", "journalist")
