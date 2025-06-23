from rest_framework import permissions

class IsOwnerOrLocatairePaiement(permissions.BasePermission):
    """
    Propriétaire : accès aux paiements de ses contrats.
    Locataire : accès à ses propres paiements.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, 'role') and user.role == 'proprietaire':
            return obj.contrat.chambre.maison.proprietaire == user
        elif hasattr(user, 'role') and user.role == 'locataire':
            return obj.contrat.locataire == user
        return False

    def has_permission(self, request, view):
        return request.user.is_authenticated 