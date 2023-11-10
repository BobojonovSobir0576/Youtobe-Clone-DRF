from django.contrib import admin
from authentification.models import CheckSmsCode


@admin.register(CheckSmsCode)
class CheckSmsAdmin(admin.ModelAdmin):
    """ Doctor Categories """
    list_display = ("author", "sms_code", "datetime", "id")