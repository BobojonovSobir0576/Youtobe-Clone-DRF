""" Django Rest Framework Library """
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage



def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'accsess': str(refresh.access_token)
    }


class Util:

    @staticmethod
    def send(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']])
        email.send()