from rest_framework import permissions

class IsLocataireOrProprietaireRendezVous(permissions.BasePermission):
    """
    Locataire : CRUD sur ses propres rendez-vous.
    Propriétaire : lecture + update statut sur ses chambres.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, 'role') and user.role == 'locataire':
            return obj.locataire == user
        elif hasattr(user, 'role') and user.role == 'proprietaire':
            return obj.chambre.maison.proprietaire == user
        return False

    def has_permission(self, request, view):
        return request.user.is_authenticated 