from django.urls import path
from authentification.views.users_views import (
    UserSignUpByEmailView,
    UserSignInView,
    CheckSmsView,
    UserProfileView,
    UserPasswordUpdate
)


urlpatterns = [
    path('sign-up/', UserSignUpByEmailView.as_view(), name='sign-up'),
    path('sign-in/', UserSignInView.as_view(), name='sign-in'),
    path('check-sms/', CheckSmsView.as_view(), name='check-sms'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password-change/', UserPasswordUpdate.as_view(), name='password-change')
]