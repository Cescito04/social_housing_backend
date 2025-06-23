from rest_framework import permissions

class IsLocataireOrProprietaireProbleme(permissions.BasePermission):
    """
    Locataire : peut signaler des problèmes sur ses contrats et voir les siens.
    Propriétaire : peut voir et mettre à jour les problèmes sur ses chambres.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, 'role') and user.role == 'locataire':
            return obj.contrat.locataire == user
        elif hasattr(user, 'role') and user.role == 'proprietaire':
            return obj.contrat.chambre.maison.proprietaire == user
        return False

    def has_permission(self, request, view):
        return request.user.is_authenticated 