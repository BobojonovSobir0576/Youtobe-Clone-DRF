""" Django Library """
from django.db import models
from django.db.models import Q

class ChannelsCategoryQuerySet(models.QuerySet):

    def filter_user(self, user):
        return self.select_related('channel_owner').filter(
            Q(channel_owner=user)
        )


class ChannelsCategoryManager(models.Manager):
    def get_queryset(self):
        return ChannelsCategoryQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)