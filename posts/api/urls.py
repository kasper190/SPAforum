from django.conf.urls import url
from .views import (
    NoteCreateAPIView,
    NoteUpdateAPIView,
    NoteDeleteAPIView,
    PostCreateAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
)


urlpatterns = [
    url(r'^create/$', PostCreateAPIView.as_view(), name='post-create'),
    url(r'^(?P<pk>\d+)/edit/$', PostUpdateAPIView.as_view(), name='post-update'),
    url(r'^(?P<pk>\d+)/delete/$', PostDeleteAPIView.as_view(), name='post-delete'),
    url(r'^note/create/$', NoteCreateAPIView.as_view(), name='note-create'),
    url(r'^note/(?P<pk>\d+)/edit/$', NoteUpdateAPIView.as_view(), name='note-update'),
    url(r'^note/(?P<pk>\d+)/delete/$', NoteDeleteAPIView.as_view(), name='note-delete'),
]