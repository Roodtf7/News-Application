"""
Signal handlers for the notifications application.
Automates email alerts and social media posts when articles transition to an approved state.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from articles.models import Article
from subscriptions.models import Subscription
from notifications.x_client import post_to_x


@receiver(pre_save, sender=Article)
def track_article_state(sender, instance, **kwargs):
    """
    Track the previous approval state of the article before saving.
    """
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._was_approved = old_instance.approved
        except sender.DoesNotExist:
            instance._was_approved = False
    else:
        instance._was_approved = False


@receiver(post_save, sender=Article)
def on_article_approved(sender, instance, created, **kwargs):
    """
    Handles side effects when an article is approved.
    Sends email notifications to subscribers and posts to X.
    Only triggers when the status actually changes to Approved.
    """
    # Check if currently approved
    if not instance.approved:
        return

    # Check if it was ALREADY approved before this save
    # If it was, we don't want to re-send notifications (e.g. typo edit)
    if getattr(instance, "_was_approved", False):
        return

    post_to_x(f"New article published: {instance.title}")

    # Fetch subscribers:
    # - subscribers to the publisher
    # - subscribers to the journalist (author)
    subs = Subscription.objects.filter(
        publisher=instance.publisher
    ) | Subscription.objects.filter(
        journalist=instance.author
    )

    emails = {
        sub.reader.email
        for sub in subs
        if sub.reader.email
    }

    if emails:
        send_mail(
            subject=f"New article published: {instance.title}",
            message=instance.body[:500],
            from_email="no-reply@newsapp.local",
            recipient_list=list(emails),
            fail_silently=True,
        )
