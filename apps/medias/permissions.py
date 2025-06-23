from rest_framework import permissions

class IsOwnerOfChambreMedia(permissions.BasePermission):
    """
    Seul le propriétaire de la chambre peut gérer les médias.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, 'role') and user.role == 'proprietaire':
            return obj.chambre.maison.proprietaire == user
        return False

    def has_permission(self, request, view):
        return request.user.is_authenticated 