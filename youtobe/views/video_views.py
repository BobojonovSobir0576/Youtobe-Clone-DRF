""" Django Library """
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

""" Django Rest Framework Library """
from rest_framework import generics, permissions, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import filters


from authentification.renderers import (
    UserRenderers
)
from youtobe.serializers.video_serializer import (
    VideoListSerializer,
    VideoDetailSerializer,
)
from youtobe.models import (
    Explore,
    Videos,
    Likes,
    Dislikes,
    ChannelsCategory,
    ChannelUser
)

class VideoSearchView(generics.ListAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideoDetailSerializer
    search_fields = ['@title',]
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    ordering_fields = '__all__'


class VideoListView(APIView):

    def get(self, request):

        queryset = Videos.objects.all()
        serializer = VideoDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        queryset = ChannelUser.objects.select_related('channel_owner').get(
            Q(channel_owner=request.user)
        )
        print(queryset)
        serializer = VideoListSerializer(
            data=request.data,)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                video=request.FILES.get('video', None),
                username=queryset
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoDetailView(APIView):

    def get(self, request, id):
        queryset = get_object_or_404(Videos, id=id)
        serializer = VideoDetailSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        queryset = get_object_or_404(Videos, id=id)
        serializer = VideoListSerializer(
            instance=queryset,
            data=request.data,
            partial=True,
            context={
                'video': request.FILES.get('video', None)
            }
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        queryset = get_object_or_404(Videos, id=id).delete()
        return Response({'msg': 'Queryset Deleted Successfully'})


class VideoGetUserView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [permissions.IsAuthenticatedOrReadOnly, AllowAny]

    def get(self, request):
        queryset = Videos.filter_user.filter_user(request.user)
        serializer = VideoDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoLikeView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [permissions.IsAuthenticatedOrReadOnly, AllowAny]

    def put(self, request, id):
        queryset = get_object_or_404(Videos, id=id)
        if request.data['like_video'] == 1:
            queryset.like_video = queryset.like_video + request.data['like_video']
            queryset.save()
            add_likes = Likes.objects.create(
                username=request.user,
                video=queryset,
                status=request.data['like_video']
            )
        serializer = VideoDetailSerializer(
            queryset
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoDisLikeView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [permissions.IsAuthenticatedOrReadOnly, AllowAny]

    def put(self, request, id):
        queryset = get_object_or_404(Videos, id=id)
        if request.data['dislike_video'] == -1:
            queryset.dislike_video = queryset.dislike_video + 1
            queryset.like_video = int(queryset.like_video) + request.data['dislike_video']
            queryset.save()
            add_dislike = Dislikes.objects.create(
                username=request.user,
                video=queryset,
                status=request.data['dislike_video']
            )
        serializer = VideoDetailSerializer(
            queryset
        )
        return Response(serializer.data, status=status.HTTP_200_OK)