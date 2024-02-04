from rest_framework.permissions import BasePermission


class IsAdminAuthenticated(BasePermission):
    # Permission personnalisée qui vérifie si l'utilisateur est authentifié en tant qu'administrateur.
    def has_permission(self, request, view):
        return bool(request.user and
                    request.user.is_authenticated and
                    request.user.is_superuser)


class IsUserSelf(BasePermission):
    # Permission personnalisée qui vérifie si l'utilisateur est le propriétaire de l'objet.
    def has_object_permission(self, request, view, obj):
        return obj == request.user
