from django.urls import path
from youtobe.views.explore_views import (
    ExploreListView
)
from youtobe.views.video_views import (
    VideoListView,
    VideoDetailView,
    VideoLikeView,
    VideoDisLikeView,
    VideoSearchView,
    VideoGetUserView
)
from youtobe.views.comment_views import (
    CommentListView,
    HistoryViews,
)
from youtobe.views.playlist_views import (
    PlayListView
)
from youtobe.views.channels_user_views import (
    ChannelsCreateView,
    ChannelsCategoryView
)


urlpatterns = [
    #explore
    path('explore-list/', ExploreListView.as_view(), name='explore'),

    #video
    path('video-list/', VideoListView.as_view(), name='video-list'),
    path('video-search/', VideoSearchView.as_view(), name='video-search'),
    path('video-get-user/', VideoGetUserView.as_view(), name='video-get-user'),
    path('video-detail/<int:id>/', VideoDetailView.as_view(), name='video-details'),
    path('video-like/<int:id>/', VideoLikeView.as_view(), name='video-like-dislike'),
    path('video-dislike/<int:id>/', VideoDisLikeView.as_view(), name='video-dislike'),

    #comment/history
    path('comment/', CommentListView.as_view(), name='comment'),
    path('history/', HistoryViews.as_view(), name='history'),

    #playlist
    path('play-list/', PlayListView.as_view(), name='play-list'),

    # channels / channels category
    path('user-channel/', ChannelsCreateView.as_view(), name='user-channel'),
    path('channel-category/', ChannelsCategoryView.as_view(), name='channel-category'),

]