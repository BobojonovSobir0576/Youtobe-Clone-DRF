from django.contrib.auth.models import Group

from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    """ User Groups Serializer """

    class Meta:
        model = Group
        fields = '__all__'