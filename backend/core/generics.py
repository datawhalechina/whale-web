from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class BasicListCreateAPIView(ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return Response({
            'data': response.data,
            'code': 0,
        })


class BasicRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        return Response({
            'data': response.data,
            'code': 0,
        })