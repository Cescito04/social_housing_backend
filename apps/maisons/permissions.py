from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Permission pour n'autoriser que le propriétaire de la maison à accéder/modifier/supprimer.
    """
    def has_object_permission(self, request, view, obj):
        return obj.proprietaire == request.user 