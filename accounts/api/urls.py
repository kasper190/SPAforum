from django.conf.urls import url
from .views import (
    UserCreateAPIView,
    UserDetailAPIView,
    UserLoginAPIView,
    UserPasswordChangeAPIView,
    UserPasswordResetAPIView,
)


urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^password-change/$', UserPasswordChangeAPIView.as_view(), name='password-change'),
    url(r'^password-reset/$', UserPasswordResetAPIView.as_view(), name='password-reset'),
    url(r'^(?P<username>[\w-]+)/$', UserDetailAPIView.as_view(), name='user-detail'),
]