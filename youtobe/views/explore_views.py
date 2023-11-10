""" Django Library """
from django.shortcuts import get_object_or_404


""" Django Rest Framework Library """
from rest_framework import generics, permissions, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from authentification.renderers import (
    UserRenderers
)
from youtobe.serializers.explore_serializer import (
    ExploreListSerializer
)
from youtobe.models import (
    Explore
)



class ExploreListView(APIView):

    def get(self, request):
        queryset = Explore.objects.all()
        serializer = ExploreListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


