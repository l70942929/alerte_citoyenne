from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Signalement
from .serializers import SignalementSerializer
from comptes.models import TransactionPoints

# ==========================================
# LISTE DES ALERTES
# ==========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liste_alertes(request):
    """Récupérer toutes les alertes"""
    alertes = Signalement.objects.all().order_by('-date_soumission')
    serializer = SignalementSerializer(alertes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detail_alerte(request, id):
    """Récupérer une alerte spécifique"""
    try:
        alerte = Signalement.objects.get(id=id)
    except Signalement.DoesNotExist:
        return Response(
            {'error': 'Alerte introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = SignalementSerializer(alerte)
    return Response(serializer.data)


# ==========================================
# SOUMISSION D'ALERTE AVEC POINTS
# ==========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def soumettre_alerte(request):
    """Soumettre une nouvelle alerte"""
    serializer = SignalementSerializer(data=request.data)
    if serializer.is_valid():
        # Sauvegarder l'alerte
        signalement = serializer.save(utilisateur=request.user)
        
        # ==========================================
        # AJOUT DES POINTS POUR LA SOUMISSION
        # ==========================================
        request.user.ajouter_points(15)
        
        TransactionPoints.objects.create(
            utilisateur=request.user,
            points=15,
            type_transaction='soumission',
            description=f"Soumission d'alerte #{signalement.id}"
        )
        # ==========================================
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# MODÉRATION D'ALERTE AVEC POINTS
# ==========================================

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def moderer_alerte(request, id):
    """Modérer une alerte (admin ou modérateur uniquement)"""
    
    # Vérifier que l'utilisateur est modérateur ou admin
    if request.user.role not in ['moderateur', 'admin']:
        return Response(
            {'error': 'Permission refusée. Vous devez être modérateur ou admin.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        signalement = Signalement.objects.get(id=id)
    except Signalement.DoesNotExist:
        return Response(
            {'error': 'Alerte introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Récupérer le nouveau statut
    nouveau_statut = request.data.get('statut')
    ancien_statut = signalement.statut
    
    # Mettre à jour l'alerte
    serializer = SignalementSerializer(signalement, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        # ==========================================
        # AJOUT DES POINTS SELON LE STATUT
        # ==========================================
        
        # Si l'alerte est vérifiée (statut passe à 'en_cours')
        if nouveau_statut == 'en_cours' and ancien_statut != 'en_cours':
            signalement.utilisateur.ajouter_points(20)
            TransactionPoints.objects.create(
                utilisateur=signalement.utilisateur,
                points=20,
                type_transaction='verification',
                description=f"Alerte #{signalement.id} vérifiée"
            )
        
        # Si l'alerte est résolue (statut passe à 'resolu')
        if nouveau_statut == 'resolu' and ancien_statut != 'resolu':
            signalement.utilisateur.ajouter_points(25)
            TransactionPoints.objects.create(
                utilisateur=signalement.utilisateur,
                points=25,
                type_transaction='resolution',
                description=f"Alerte #{signalement.id} résolue"
            )
        
        # Si l'alerte est marquée "retrouvé" (statut passe à 'retrouve')
        if nouveau_statut == 'retrouve' and ancien_statut != 'retrouve':
            signalement.utilisateur.ajouter_points(30)
            TransactionPoints.objects.create(
                utilisateur=signalement.utilisateur,
                points=30,
                type_transaction='retrouve',
                description=f"Objet/personne retrouvé(e) - Alerte #{signalement.id}"
            )
        # ==========================================
        
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# SUPPRESSION D'ALERTE
# ==========================================

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supprimer_alerte(request, id):
    """Supprimer une alerte (admin ou propriétaire)"""
    try:
        signalement = Signalement.objects.get(id=id)
    except Signalement.DoesNotExist:
        return Response(
            {'error': 'Alerte introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Vérifier les permissions
    if request.user.role not in ['admin', 'moderateur'] and signalement.utilisateur != request.user:
        return Response(
            {'error': 'Vous n\'êtes pas autorisé à supprimer cette alerte.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    signalement.delete()
    return Response(
        {'message': 'Alerte supprimée avec succès'},
        status=status.HTTP_200_OK
    )


# ==========================================
# STATISTIQUES DES ALERTES
# ==========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistiques_alertes(request):
    """Récupérer les statistiques des alertes"""
    total = Signalement.objects.count()
    en_attente = Signalement.objects.filter(statut='recu').count()
    en_cours = Signalement.objects.filter(statut='en_cours').count()
    resolu = Signalement.objects.filter(statut='resolu').count()
    cloture = Signalement.objects.filter(statut='cloture').count()
    
    return Response({
        'total': total,
        'en_attente': en_attente,
        'en_cours': en_cours,
        'resolu': resolu,
        'cloture': cloture
    })