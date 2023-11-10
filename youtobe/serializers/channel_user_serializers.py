""" Django Rest Framework Library """
from rest_framework import serializers

""" Authentification Serializer """
from authentification.serializers.users_serializers import (
    UserProfileSerializer
)
from youtobe.models import (
    ChannelUser,
    ChannelsCategory
)


class ChannelsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelsCategory
        fields = '__all__'


class ChannelsListSerializer(serializers.ModelSerializer):
    channel_owner = UserProfileSerializer(read_only=True)
    channel_users = UserProfileSerializer(read_only=True, many=True)
    channel_category = ChannelsCategorySerializer(read_only=True)

    class Meta:
        model = ChannelUser
        fields = [
            'channel_owner',
            'channel_users',
            'channel_name',
            'channel_category',
            'date'
        ]


class ChannelsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChannelUser
        fields = [
            'channel_owner',
            'channel_users',
            'channel_name',
            'channel_category',
            'date'
        ]

        def create(self, validated_data):
            create = ChannelUser.objects.create(**validated_data)
            return create