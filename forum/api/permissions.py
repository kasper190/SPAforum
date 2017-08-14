from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True
        
        is_moderator = obj.subforum.moderators.filter(id=request.user.id).exists()
        return is_moderator