from rest_framework import permissions


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
