"""
Models for the articles application.
Defines the structure for Articles and Newsletters, including approval workflows and authorship.
"""
from django.conf import settings
from django.db import models
from publishers.models import Publisher
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Article(models.Model):
    """
    Represents a news article written by a journalist.
    Articles require editorial approval before being published.
    """
    title = models.CharField(max_length=255)
    body = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    # If True, article is published independently (visible to readers immediately)
    # If False and publisher exists, requires editor approval
    is_independent = models.BooleanField(default=False)

    approved = models.BooleanField(default=False)

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_articles",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def approve(self, editor):
        """
        Approve the article and set the publication date.
        
        :param editor: The user (editor) who approves the article.
        """
        self.approved = True
        self.approved_by = editor
        self.published_at = timezone.now()
        self.save(update_fields=["approved", "approved_by", "published_at"])

    def __str__(self):
        """
        Return the string representation of the article.
        """
        return self.title


class Newsletter(models.Model):
    """
    Represents a newsletter published by a journalist to readers.
    Supports optional editorial approval if associated with a publisher.
    """
    title = models.CharField(max_length=255)
    body = models.TextField()
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="newsletters",
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    is_independent = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_newsletters",
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    def approve(self, editor):
        """
        Approve the newsletter.
        """
        self.approved = True
        self.approved_by = editor
        self.published_at = timezone.now()
        self.save(update_fields=["approved", "approved_by", "published_at"])

    def __str__(self):
        """
        Return the string representation of the newsletter.
        """
        return self.title