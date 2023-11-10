""" Django Rest Framework Library """
from rest_framework import serializers

""" Authentification Serializer """
from authentification.serializers.users_serializers import (
    UserProfileSerializer
)

from youtobe.models import (
    Playlist
)
from youtobe.serializers.video_serializer import (
    VideoListSerializer,
    VideoDetailSerializer,
)
from authentification.serializers.users_serializers import (
    UserProfileSerializer
)


class PlayListSeralizer(serializers.ModelSerializer):
    playlist_owner = UserProfileSerializer(read_only=True)
    playlist_videos = VideoDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Playlist
        fields = [
            'playlist_name',
            'playlist_videos',
            'playlist_owner',
            'created_date'
        ]


class PlayListCreateSeralizer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = [
            'playlist_name',
            'playlist_videos',
            'playlist_owner',
            'created_date'
        ]

        def create(self, validated_data):
            create = Playlist.objects.create(**validated_data)
            for k in validated_data.pop('playlist_videos'):
                create.playlist_videos.add(k)
                create.save()
            return create