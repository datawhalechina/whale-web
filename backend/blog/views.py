import logging

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
import shortuuid
from rest_framework import status
from rest_framework.response import Response

from .serializers import ArticleSerializer
from .models import Article
from core.permissions import ReadOnly
from core.generics import BasicListCreateAPIView, BasicRetrieveUpdateDestroyAPIView

logger = logging.getLogger(__name__)


class ArticleListCreateView(BasicListCreateAPIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data['id'] = shortuuid.uuid()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'data': serializer.data,
                'code': 0,
            },
            status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetailView(BasicRetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()