from rest_framework import permissions
user_role = ['moderator', 'admin']


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin))


class OnlyReadOrСhangeAuthorAdminModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role in user_role
            or obj.author == request.user
            or request.user.is_staff == 1)


class OwnIsAuthenticatedAndIsAdmin(permissions.IsAuthenticated):
    """Добавлять юзеров может admin"""

    def has_permission(self, request, view):
        try:
            return request.user.role == 'admin'
        except:
            return False


# class UpdRoleOnlyAdmin(permissions.IsAuthenticated):
#     """user не может изменять свою role"""
#
#     def has_permission(self, request, view):
#         if request.method not in permissions.SAFE_METHODS:
#             if request.user.role == 'user':
#                 return 'role' not in request.data
#         return True

