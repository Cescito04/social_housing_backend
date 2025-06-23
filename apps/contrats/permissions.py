from rest_framework import permissions

class IsOwnerOrLocataire(permissions.BasePermission):
    """
    Propriétaire : accès aux contrats de ses chambres.
    Locataire : accès à ses propres contrats.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, 'role') and user.role == 'proprietaire':
            return obj.chambre.maison.proprietaire == user
        elif hasattr(user, 'role') and user.role == 'locataire':
            return obj.locataire == user
        return False

    def has_permission(self, request, view):
        return request.user.is_authenticated 