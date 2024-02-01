from rest_framework.permissions import BasePermission


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and
                    request.user.is_authenticated and
                    request.user.is_superuser)


class IsUserSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
