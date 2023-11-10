""" Django Rest Framework Library """
from rest_framework import serializers

""" Authentification Serializer """
from youtobe.serializers.channel_user_serializers import (
    ChannelsListSerializer
)
from youtobe.models import (
    Explore,
    Videos
)
from youtobe.serializers.explore_serializer import (
    ExploreListSerializer
)


class VideoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Videos
        fields = [
            'id',
            'username',
            'video',
            'title',
            'explores',
            'keywords',
            'like_video',
            'dislike_video',
            'description'
        ]

        def create(self, validated_data):
            create = Videos.objects.create(**validated_data)
            return create

        def update(self, instance, validated_data):
            instance.model_method()
            update = super().update(instance, validated_data)
            if self.context.get('video') == None:
                update.video = instance.avatar
            else:
                update.video = self.context.get('video')
                update.save()
            return update


class VideoDetailSerializer(serializers.ModelSerializer):
    username = ChannelsListSerializer(read_only=True)
    explores = ExploreListSerializer(read_only=True)

    class Meta:
        model = Videos
        fields = [
            'id',
            'username',
            'video',
            'title',
            'explores',
            'keywords',
            'like_video',
            'dislike_video',
            'description',
            'post_date'
        ]