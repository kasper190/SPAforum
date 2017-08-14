from django.conf.urls import url
from .views import (
    CategoryListAPIView,
    ForumDetailAPIView,
    SubforumDetailAPIView,
    ThreadCreateAPIView,
    ThreadDeleteAPIView,
    ThreadDetailAPIView,
    ThreadUpdateAPIView,
)


urlpatterns = [ 
    url(r'^descriptions/$', ForumDetailAPIView.as_view(), name='forum-detail'),
    url(r'^categories/$', CategoryListAPIView.as_view(), name='category-list'),
    url(r'^(?P<subforum_slug>[\w-]+)/$', SubforumDetailAPIView.as_view(), name='subforum-detail'),
    url(r'^thread/create/$', ThreadCreateAPIView.as_view(), name='thread-create'),
    url(r'^(?P<subforum_slug>[\w\-]+)/(?P<thread_slug>[\w\-]+)/$', ThreadDetailAPIView.as_view(), name='thread-detail'),
    url(r'^(?P<subforum_slug>[\w\-]+)/(?P<thread_slug>[\w\-]+)/edit/$', ThreadUpdateAPIView.as_view(), name='thread-update'),
    url(r'^(?P<subforum_slug>[\w\-]+)/(?P<thread_slug>[\w\-]+)/delete/$', ThreadDeleteAPIView.as_view(), name='thread-delete'),
]