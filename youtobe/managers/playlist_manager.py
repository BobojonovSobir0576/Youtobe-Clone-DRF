""" Django Library """
from django.db import models
from django.db.models import Q

class PlayListQuerySet(models.QuerySet):

    def filter_user(self, user):
        return self.select_related('playlist_owner').filter(
            Q(playlist_owner=user)
        )


class PlayListManager(models.Manager):
    def get_queryset(self):
        return PlayListQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)