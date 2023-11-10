""" Django Library """
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import reverse
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


""" Django Rest Framework Library """
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

""" Serilizers list """
from authentification.serializers.groups_serializers import (
    GroupSerializer
)



class UserProfileSerializer(serializers.ModelSerializer):
    """ User Profile """

    groups = GroupSerializer(read_only=True, many=True)


    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'groups',
            'date_joined'
        ]


class UserSignUpByEmailSerializer(serializers.ModelSerializer):
    """ User sign Up By Email """
    password = serializers.CharField(max_length=68, min_length=6, write_only=True, validators=[validate_password])
    email = serializers.EmailField(
        max_length=255,
        write_only=False,
        allow_null=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'groups',
            'username',
            'password'
        )

        def create(self, validated_data):

            create = User.objects.create_user(**validated_data)
            create.set_password(validated_data['password'])
            groups = Group.objects.filter(name=['User'])
            for i in groups:
                create.groups.add(i)
            create.save()
            return create

        def update(self, instance, validated_data):
            instance.model_method()
            update = super().update(instance, validated_data)
            # update.set_password(validated_data['password'])
            return update


class UserSignInSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255,
        write_only=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = ['username', 'password']
        read_only_fields = ('username',)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')