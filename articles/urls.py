"""
URL routing for the articles application.
Defines paths for viewing, creating, and managing articles and newsletters.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Editorial workflows
    path("editor/articles/", views.pending_articles, name="pending-articles"),
    path(
        "editor/articles/<int:article_id>/approve/",
        views.approve_article,
        name="approve-article"),
    path(
        "editor/newsletters/<int:newsletter_id>/approve/",
        views.approve_newsletter,
        name="approve-newsletter"),

    # Feed and details
    path("articles/", views.article_list, name="article-list"),
    path("articles/create/", views.create_article, name="create-article"),
    path("articles/<int:article_id>/", views.article_detail, name="article-detail"),
    path("articles/<int:article_id>/update/", views.update_article, name="update-article"),
    path("articles/<int:article_id>/delete/", views.delete_article, name="delete-article"),
    
    # Newsletter management
    path("newsletters/create/", views.create_newsletter, name="create-newsletter"),
    path("newsletters/<int:newsletter_id>/", views.newsletter_detail, name="newsletter-detail"),
    path("newsletters/<int:newsletter_id>/update/", views.update_newsletter, name="update-newsletter"),
    path("newsletters/<int:newsletter_id>/delete/", views.delete_newsletter, name="delete-newsletter"),
]
