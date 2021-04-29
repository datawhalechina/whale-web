from rest_framework.viewsets import GenericViewSet
from .generics import BasicListCreateAPIView, BasicRetrieveUpdateDestroyAPIView


class BasicListCreateViewSet(BasicListCreateAPIView, GenericViewSet):
    pass


class BasicRetrieveUpdateDestroyViewSet(BasicRetrieveUpdateDestroyAPIView, GenericViewSet):
    pass