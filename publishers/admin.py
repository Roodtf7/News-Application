"""
Admin configuration for the publishers application.
Allows administrative management of Publisher organizations and their members.
"""
from django.contrib import admin
from .models import Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Publisher model.
    """
    list_display = ("name",)
