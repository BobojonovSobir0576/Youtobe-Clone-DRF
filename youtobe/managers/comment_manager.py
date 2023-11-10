""" Django Library """
from django.db import models
from django.db.models import Q

class CommentQuerySet(models.QuerySet):

    def filter_user(self, user):
        return self.select_related('username').filter(
            Q(username=user)
        )


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)