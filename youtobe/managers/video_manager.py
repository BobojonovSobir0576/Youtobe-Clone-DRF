""" Django Library """
from django.db import models
from django.db.models import Q

class VideosQuerySet(models.QuerySet):

    def filter_user(self, user):
        return self.select_related('username').filter(
            Q(username__channel_owner=user)
        )


class VideosManager(models.Manager):
    def get_queryset(self):
        return VideosQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)