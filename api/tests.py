"""
Tests for the API application.
Validates the functionality of API endpoints, security permissions, and response formats.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from articles.models import Article
from publishers.models import Publisher
from subscriptions.models import Subscription

User = get_user_model()


class SubscribedArticlesAPITest(TestCase):
    """
    Test suite for the SubscribedArticlesView API endpoint.
    Validates subscription-based article filtering and authentication.
    """
    def setUp(self):
        """
        Set up test data including users, publishers, articles, and subscriptions.
        """
        self.client = APIClient()

        self.reader = User.objects.create_user(
            username="reader",
            password="testpass",
            role="reader",
        )
        self.journalist = User.objects.create_user(
            username="journalist",
            password="testpass",
            role="journalist",
        )
        self.publisher = Publisher.objects.create(name="Test Publisher")

        self.article = Article.objects.create(
            title="Approved Article",
            body="Some content",
            author=self.journalist,
            publisher=self.publisher,
            approved=True,
        )
        Subscription.objects.create(
            reader=self.reader,
            publisher=self.publisher,
        )
        self.client.login(username="reader", password="testpass")

    def test_reader_sees_subscribed_articles(self):
        """
        Test that a reader can see articles from publishers they are subscribed to.
        """
        response = self.client.get("/api/articles/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_reader_does_not_see_unsubscribed_articles(self):
        """
        Test that a reader does not see articles from publishers they are not subscribed to.
        """
        other_publisher = Publisher.objects.create(name="Other Publisher")

        Article.objects.create(
            title="Hidden Article",
            body="Hidden",
            author=self.journalist,
            publisher=other_publisher,
            approved=True,
        )

        response = self.client.get("/api/articles/")
        self.assertEqual(len(response.data), 1)

    def test_unapproved_articles_not_returned(self):
        """
        Test that unapproved articles are not returned in the API response.
        """
        Article.objects.create(
            title="Draft Article",
            body="Draft",
            author=self.journalist,
            publisher=self.publisher,
            approved=False,
        )

        response = self.client.get("/api/articles/")
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_user_blocked(self):
        """
        Test that unauthenticated users are blocked from accessing the API.
        """
        self.client.logout()
        response = self.client.get("/api/articles/")
        self.assertEqual(response.status_code, 403)

    def test_reader_sees_journalist_subscribed_articles(self):
        """
        Test that a reader sees articles from journalists they are subscribed to,
        even if not subscribed to the publisher.
        """
        # Create an article by a journalist the reader is NOT subscribed to publisher but IS subscribed to journalist
        other_journalist = User.objects.create_user(username="other_j", password="pw", role="journalist")
        Article.objects.create(
            title="Journalist Article",
            body="Content",
            author=other_journalist,
            approved=True
        )
        
        # Initially should not see it (already has 1 from setUp publisher sub)
        response = self.client.get("/api/articles/")
        self.assertEqual(len(response.data), 1)

        # Subscribe to journalist
        Subscription.objects.create(reader=self.reader, journalist=other_journalist)
        
        # Now should see both
        response = self.client.get("/api/articles/")
        self.assertEqual(len(response.data), 2)

    def test_api_returns_xml(self):
        """
        Test that the API can return XML format when requested via Accept header.
        """
        # Explicitly request XML
        response = self.client.get("/api/articles/", HTTP_ACCEPT='application/xml')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('application/xml'))
        # Check if it starts with xml or has root tag
        self.assertIn(b'<root>', response.content)
        self.assertIn(b'<article>', response.content)





