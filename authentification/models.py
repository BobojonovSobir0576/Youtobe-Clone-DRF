from django.db import models
from django.contrib.auth.models import User


class CheckSmsCode(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_sms')
    sms_code = models.IntegerField(default=0, null=False, blank=False)
    datetime = models.DateTimeField(auto_now_add=True)
