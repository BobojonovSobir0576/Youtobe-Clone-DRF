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
    Explore,
    Videos,
    Comments,
    UserViews,
    ChannelUser,
    ChannelsCategory
)
from youtobe.serializers.channel_user_serializers import (
    ChannelsListSerializer,
    ChannelsCreateSerializer,
    ChannelsCategorySerializer
)


class ChannelsCategoryView(APIView):

    def get(self, request):
        queryset = ChannelsCategory.objects.all()
        serializer = ChannelsCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChannelsCreateView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [permissions.IsAuthenticatedOrReadOnly, AllowAny]

    def get(self, request):
        queryset = ChannelUser.filter_user.filter_user(request.user)
        serializer = ChannelsListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = ChannelsCreateSerializer(
            data=request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
           get_user_channel = ChannelUser.objects.select_related('channel_owner').filter(channel_owner=request.user)
           if get_user_channel:
               return Response({'error':'Username already channel done...'})
           serializer.save(
                channel_owner=request.user
            )
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

