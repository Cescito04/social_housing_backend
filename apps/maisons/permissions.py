from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Permission pour n'autoriser que le propriétaire de la maison à accéder/modifier/supprimer.
    Autorise tout utilisateur authentifié à faire un POST (création).
    """
    def has_permission(self, request, view):
        # Autoriser tout utilisateur authentifié à faire un POST
        if request.method == 'POST':
            return request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'proprietaire'
        return True

    def has_object_permission(self, request, view, obj):
        return obj.proprietaire == request.user 