from django.db import models
from django.contrib.auth.models import User

from youtobe.managers.comment_manager import (
    CommentManager
)
from youtobe.managers.history_manager import (
    HistoryManager
)
from youtobe.managers.playlist_manager import (
    PlayListManager
)
from youtobe.managers.channels_category_manager import (
    ChannelsCategoryManager
)
from youtobe.managers.video_manager import (
    VideosManager
)

class ChannelsCategory(models.Model):
    channels_category = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.channels_category


class ChannelUser(models.Model):
    channel_owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255, null=True, blank=True)
    channel_users = models.ManyToManyField(User, null=True, blank=True, related_name='users')
    channel_category = models.ForeignKey(ChannelsCategory, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    objects = models.Manager()
    filter_user = ChannelsCategoryManager()

    def __str__(self):
        return self.channel_name


class Explore(models.Model):
    explore = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.explore


class Videos(models.Model):
    username = models.ForeignKey(ChannelUser, on_delete=models.CASCADE, null=True,blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    explores = models.ForeignKey(Explore, on_delete=models.CASCADE)
    keywords = models.CharField(max_length=255, default='')
    like_video = models.IntegerField(default=0)
    dislike_video = models.IntegerField(default=0)
    description = models.TextField()
    post_date = models.DateTimeField(auto_now=True, blank=True)

    objects = models.Manager()
    filter_user = VideosManager()

    def __str__(self):
        return self.title


class Comments(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, null=True, blank=True)
    describe = models.TextField(null=True)
    post_date = models.DateTimeField(blank=True, auto_now=True)

    objects = models.Manager()
    filter_user = CommentManager()

    def __str__(self):
        self.save()
        return 'Comment %s by %s' % (self.describe, self.username)


class Likes(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.username) + ' like'


class Dislikes(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.username + ' dislike'


class UserViews(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, null=True, blank=True)
    post_date = models.DateTimeField(blank=True, auto_now=True)


    objects = models.Manager()
    filter_user = HistoryManager()

    def __str__(self):
        return self.username + ' view'


class Playlist(models.Model):
    playlist_name = models.CharField(max_length=50,default="new playlist")
    playlist_videos = models.ManyToManyField(Videos, null=True)
    playlist_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    filter_user = PlayListManager()

    def __str__(self):
        return self.playlist_name