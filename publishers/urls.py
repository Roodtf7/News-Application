"""
URL routing for the publishers application.
Defines paths for listing publishers and managing their internal roles.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("publishers/", views.publisher_list, name="publisher-list"),
    path("publishers/create/", views.create_publisher, name="create-publisher"),
    path("publishers/<int:publisher_id>/", views.publisher_detail, name="publisher-detail"),
    path("publishers/<int:publisher_id>/add-editor/", views.add_editor, name="add-editor"),
    path("publishers/<int:publisher_id>/join/", views.join_publisher, name="join-publisher"),
]
