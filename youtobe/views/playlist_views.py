""" Django Library """
from django.shortcuts import get_object_or_404
from django.db.models import Q

""" Django Rest Framework Library """
from rest_framework import generics, permissions, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from authentification.renderers import (
    UserRenderers
)

from youtobe.models import (
    Playlist
)
from youtobe.serializers.playlist_serializer import (
    PlayListSeralizer,
    PlayListCreateSeralizer
)


class PlayListView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [permissions.IsAuthenticatedOrReadOnly, AllowAny]

    def get(self, request):
        queryset = Playlist.filter_user.filter_user(request.user).order_by('-id')
        serializer = PlayListSeralizer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PlayListCreateSeralizer(
            data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(playlist_owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
