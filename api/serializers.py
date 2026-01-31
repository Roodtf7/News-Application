"""
Serializers for the API application.
Handles the conversion of complex model instances into native Python datatypes for JSON and XML responses.
"""
from rest_framework import serializers
from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model to be used in API responses.
    """
    author = serializers.StringRelatedField()
    publisher = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "body",
            "author",
            "publisher",
            "published_at",
        ]
