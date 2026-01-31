"""
Views for the API application.
Implements the business logic for responding to API requests and filtering data based on permissions.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from articles.models import Article
from subscriptions.models import Subscription
from .serializers import ArticleSerializer
from .renderers import MiniXMLRenderer


class SubscribedArticlesView(APIView):
    """
    Provides a read-only API endpoint for retrieving published articles.
    """
    permission_classes = [IsAuthenticated]
    renderer_classes = APIView.renderer_classes + [MiniXMLRenderer]


    def get(self, request):
        """
        Handle GET requests to retrieve articles from subscribed publishers and journalists.
        """
        user = request.user

        # Get subscriptions
        publisher_ids = Subscription.objects.filter(
            reader=user,
            publisher__isnull=False
        ).values_list("publisher_id", flat=True)

        journalist_ids = Subscription.objects.filter(
            reader=user,
            journalist__isnull=False
        ).values_list("journalist_id", flat=True)

        # Get approved articles
        articles = Article.objects.filter(
            approved=True
        ).filter(
            publisher_id__in=publisher_ids
        ) | Article.objects.filter(
            approved=True,
            author_id__in=journalist_ids
        )

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
