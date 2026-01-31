"""
Admin configuration for the articles application.
Customizes the display and management of Articles and Newsletters in the Django admin.
"""
from django.contrib import admin
from articles.models import Article, Newsletter


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Article model.
    """
    list_display = ("title", "author", "approved", "is_independent", "published_at")
    list_filter = ("approved", "is_independent")
    actions = ["approve_selected"]

    def approve_selected(self, request, queryset):
        """
        Action to approve a selection of articles.
        """
        for article in queryset:
            if not article.approved:
                article.approve(editor=request.user)

    approve_selected.short_description = "Approve selected articles"


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Newsletter model.
    """
    list_display = ("title", "author", "approved", "is_independent", "published_at")
    list_filter = ("approved", "is_independent")
    actions = ["approve_selected"]

    def approve_selected(self, request, queryset):
        """
        Action to approve a selection of newsletters.
        """
        for newsletter in queryset:
            if not newsletter.approved:
                newsletter.approve(editor=request.user)

    approve_selected.short_description = "Approve selected newsletters"

