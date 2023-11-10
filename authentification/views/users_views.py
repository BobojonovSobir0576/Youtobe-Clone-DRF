""" Django Library """
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.models import *
from datetime import date, timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

""" Django Rest Framework Library """
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed


""" Serilizers list """
import random, jwt
from authentification.serializers.users_serializers import (
    UserProfileSerializer,
    UserSignUpByEmailSerializer,
    UserSignInSerializer,
    LogoutSerializer
)

from authentification.utils import (
    get_token_for_user,
    Util
)
from authentification.models import (
    CheckSmsCode
)
from authentification.renderers import (
    UserRenderers
)





class UserSignUpByEmailView(generics.GenericAPIView):

    serializer_class = UserSignUpByEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserSignInView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignInSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            username = request.data['username']
            password = request.data['password']
            if username == '' or password=='':
                return Response({'error':{'none_filed_error':['Username or Password is not write']}}, status=status.HTTP_204_NO_CONTENT)

            user = authenticate(username=username, password=password)

            if not user:
                return Response({'error': ('Invalid credentials, try again')}, status=status.HTTP_400_BAD_REQUEST)

            token = get_token_for_user(user)
            sms_number_random = str(random.randint(10000, 99999))
            email_body = f'HI {user.username}, \n This is your varification code:  {sms_number_random}.'

            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Verify your email'
            }

            Util.send(data)
            add_sms_code = CheckSmsCode(
                author=user,
                sms_code=sms_number_random
            ).save()
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckSmsView(APIView):
    """ Views """
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]

    def post(self, request):
        sms_code = request.data["sms_code"]
        if sms_code == "":
            context = {"Code not entered"}
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)
        code_objects = CheckSmsCode.objects.latest("id")
        if int(sms_code) == int(code_objects.sms_code):
            context = {"Welcome to the system !"}
            return Response({'context':context, 'status': True}, status=status.HTTP_200_OK)
        return Response(
            {"error": "SMS code error", "status": False},
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
        )


class UserProfileView(APIView):

    render_classes = [UserRenderers]
    perrmisson_class = [permissions.IsAuthenticatedOrReadOnly, AllowAny]

    def get(self, request):
        try:
            serializers = UserProfileSerializer(request.user)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as indetifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as indetifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':serializers.data},status=status.HTTP_200_OK)

    def put(self, request):
        try:
            serializers = UserSignUpByEmailSerializer(instance=request.user, data=request.data, partial=True)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError as indetifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as indetifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':serializers.data},status=status.HTTP_200_OK)


class UserPasswordUpdate(APIView):

    render_classes = [UserRenderers]
    perrmisson_class = [permissions.IsAuthenticatedOrReadOnly, AllowAny]

    def put(self, request):
        try:

            serializers = UserSignUpByEmailSerializer(
                instance=request.user,
                data=request.data, partial=True)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                user = User.objects.get(username = request.user.username)
                sms_number_random = str(random.randint(10000, 99999))
                email_body = (f'HI {user.username}, \n '
                              f'This is your varification code:  '
                              f'{sms_number_random}.')

                data = {
                    'email_body': email_body,
                    'to_email': user.email,
                    'email_subject': 'Verify your email'
                }

                Util.send(data)
                add_sms_code = CheckSmsCode(
                    author=user,
                    sms_code=sms_number_random
                ).save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError as indetifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as indetifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':serializers.data},status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    perrmisson_class = [permissions.IsAuthenticatedOrReadOnly, AllowAny]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)