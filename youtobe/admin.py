from youtobe.models import (
    Explore,
    Videos,
    Comments,
    Likes,
    Dislikes,
    UserViews,
    Playlist,
    ChannelUser,
    ChannelsCategory
)
from django.contrib import admin

admin.site.register(ChannelsCategory)
admin.site.register(ChannelUser)
admin.site.register(Explore)
admin.site.register(Videos)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Dislikes)
admin.site.register(UserViews)
admin.site.register(Playlist)

