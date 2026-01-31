from django.test import TestCase
from django.contrib.auth import get_user_model
from articles.models import Article, Newsletter
from publishers.models import Publisher
from subscriptions.models import Subscription

User = get_user_model()


class UserRoleTests(TestCase):
    """
    Test suite for validating role-based properties and permissions in the User model.
    """
    def setUp(self):
        """
        Set up test users with different roles (reader, journalist, editor) and a test publisher.
        """
        self.reader = User.objects.create_user(
            username="reader", role="reader", password="password"
        )
        self.journalist = User.objects.create_user(
            username="journalist", role="journalist", password="password"
        )
        self.editor = User.objects.create_user(
            username="editor", role="editor", password="password"
        )
        self.publisher = Publisher.objects.create(name="Test Publisher")

    def test_reader_properties(self):
        """
        Test that a Reader has access to subscriptions but returns None for journalist fields.
        """
        Subscription.objects.create(reader=self.reader, publisher=self.publisher)
        
        # Should have subscriptions
        self.assertIsNotNone(self.reader.reader_subscriptions)
        self.assertEqual(self.reader.reader_subscriptions.count(), 1)

        # Should NOT have journalist fields
        self.assertIsNone(self.reader.journalist_articles)
        self.assertIsNone(self.reader.journalist_newsletters)

    def test_journalist_properties(self):
        """
        Test that a Journalist has access to authored items but returns None for reader fields.
        """
        Article.objects.create(
            title="My Article", body="...", author=self.journalist, is_independent=True
        )
        
        # Should have articles
        self.assertIsNotNone(self.journalist.journalist_articles)
        self.assertEqual(self.journalist.journalist_articles.count(), 1)

        # Should NOT have reader fields
        self.assertIsNone(self.journalist.reader_subscriptions)

    def test_editor_properties(self):
        """
        Test that an Editor (who is neither pure reader nor journalist in this context) 
        returns None for specific role fields if not applicable.
        """
        # Based on current logic, editor is not "reader" or "journalist"
        self.assertIsNone(self.editor.reader_subscriptions)
        self.assertIsNone(self.editor.journalist_articles)
