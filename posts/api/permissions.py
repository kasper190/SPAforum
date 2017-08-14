from rest_framework.permissions import BasePermission, SAFE_METHODS
from posts.models import (
    Post,
    Note,
)


class IsAdminOrModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        is_moderator = False
        if type(obj) is Post:
            is_moderator = obj.thread.subforum.moderators.filter(id=request.user.id).exists()
        if type(obj) is Note:
            is_moderator = obj.post.thread.subforum.moderators.filter(id=request.user.id).exists()
        return is_moderator


class IsOwnerOrAdminOrModeratorOrReadOnly(IsAdminOrModeratorOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return super(IsOwnerOrAdminOrModeratorOrReadOnly, self).has_object_permission(request, view, obj)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user