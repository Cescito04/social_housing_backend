from rest_framework import permissions

class IsOwnerOfMaison(permissions.BasePermission):
    """
    Permission pour n'autoriser que le propriétaire de la maison à gérer ses chambres.
    """
    def has_object_permission(self, request, view, obj):
        return obj.maison.proprietaire == request.user

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'proprietaire' 