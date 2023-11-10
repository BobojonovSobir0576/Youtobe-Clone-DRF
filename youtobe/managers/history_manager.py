""" Django Library """
from django.db import models
from django.db.models import Q

class HistoryQuerySet(models.QuerySet):

    def filter_user(self, user):
        return self.select_related('username').filter(
            Q(username=user)
        )


class HistoryManager(models.Manager):
    def get_queryset(self):
        return HistoryQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)