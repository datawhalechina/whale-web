from rest_framework import serializers
from .models import Article
from core.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='email'
     )
    class Meta:
        model = Article
        fields = (
            'id',
            'author',
            'title',
            'content',
            'created_at',
            'updated_at',
            'status',
        )
