from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

user_role = ['moderator', 'admin']


class OnlyReadOrСhangeAuthorAdminModerator(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.role in user_role
            or obj.author == request.user
            or request.user.is_staff == True
        )
