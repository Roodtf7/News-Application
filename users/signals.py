"""
Signal handlers for the users application.
Automatically assigns users to the correct Django Permission Groups based on their selected role.
"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from articles.models import Article
from .models import User


def setup_groups():
    """
    Set up user groups (Readers, Journalists, Editors) with appropriate permissions.
    Creates groups if they don't exist and assigns article-related permissions.
    """
    article_ct = ContentType.objects.get_for_model(Article)

    reader_group, _ = Group.objects.get_or_create(name="Readers")
    journalist_group, _ = Group.objects.get_or_create(name="Journalists")
    editor_group, _ = Group.objects.get_or_create(name="Editors")

    view_perm = Permission.objects.get(codename="view_article", content_type=article_ct)
    add_perm = Permission.objects.get(codename="add_article", content_type=article_ct)
    change_perm = Permission.objects.get(codename="change_article", content_type=article_ct)
    delete_perm = Permission.objects.get(codename="delete_article", content_type=article_ct)

    reader_group.permissions.set([view_perm])

    journalist_group.permissions.set([
        view_perm, add_perm, change_perm, delete_perm
    ])

    editor_group.permissions.set([
        view_perm, change_perm, delete_perm
    ])


@receiver(post_save, sender=User)
def assign_user_group(sender, instance, created, **kwargs):
    """
    Signal handler to automatically assign a user to the appropriate group based on their role.
    Triggered after a User instance is saved.
    """
    setup_groups()

    role_group_map = {
        "reader": "Readers",
        "journalist": "Journalists",
        "editor": "Editors",
    }

    group_name = role_group_map.get(instance.role)

    if group_name:
        group = Group.objects.get(name=group_name)
        instance.groups.clear()
        instance.groups.add(group)
