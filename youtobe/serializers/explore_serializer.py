""" Django Rest Framework Library """
from rest_framework import serializers

""" Authentification Serializer """
from authentification.serializers.users_serializers import (
    UserProfileSerializer
)
from youtobe.models import (
    Explore,
)


class ExploreListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Explore
        fields = ['explore', 'id']