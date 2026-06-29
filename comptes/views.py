from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .models import Utilisateur, TransactionPoints
from .serializers import InscriptionSerializer, UtilisateurSerializer, TransactionPointsSerializer
import re

# ==========================================
# AUTHENTIFICATION
# ==========================================

@api_view(['POST'])
@permission_classes([AllowAny])
def inscription(request):
    serializer = InscriptionSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'role': user.role,
            'points': user.points
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def connexion(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'role': user.role,
            'points': user.points
        })
    return Response(
        {'erreur': 'Identifiants incorrects'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deconnexion(request):
    request.user.auth_token.delete()
    return Response({'message': 'Déconnecté avec succès'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liste_utilisateurs(request):
    users = Utilisateur.objects.exclude(id=request.user.id)
    serializer = UtilisateurSerializer(users, many=True)
    return Response(serializer.data)


# ==========================================
# MOT DE PASSE OUBLIÉ
# ==========================================

@api_view(['POST'])
@permission_classes([AllowAny])
def mot_de_passe_oublie(request):
    """Envoyer un email de réinitialisation de mot de passe"""
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'L\'email est requis.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Vérifier que l'email est valide
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return Response(
            {'error': 'Veuillez entrer un email valide.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = Utilisateur.objects.get(email=email)
    except Utilisateur.DoesNotExist:
        # Pour des raisons de sécurité, on ne révèle pas si l'email existe
        return Response(
            {'message': 'Si cet email existe, un email de réinitialisation a été envoyé.'},
            status=status.HTTP_200_OK
        )
    
    # Générer le token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Créer le lien de réinitialisation
    reset_link = f"https://alerte-frontend-47hgoxtzk-tchamko-larrissa-merveille-s-projects.vercel.app/reinitialiser-mot-de-passe?uid={uid}&token={token}"
    
    # Envoyer l'email
    try:
        send_mail(
            subject='Réinitialisation de votre mot de passe - CIVIALERT',
            message=f"""
Bonjour {user.username},

Vous avez demandé la réinitialisation de votre mot de passe sur CIVIALERT.

Cliquez sur le lien ci-dessous pour créer un nouveau mot de passe :
{reset_link}

Si vous n'avez pas fait cette demande, ignorez cet email.

Cordialement,
L'équipe CIVIALERT
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(
            {'message': 'Un email de réinitialisation vous a été envoyé.'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de l\'envoi de l\'email: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def reinitialiser_mot_de_passe(request):
    """Réinitialiser le mot de passe avec uid et token"""
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    
    if not uid or not token or not new_password:
        return Response(
            {'error': 'UID, token et nouveau mot de passe sont requis.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(new_password) < 6:
        return Response(
            {'error': 'Le mot de passe doit contenir au moins 6 caractères.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = Utilisateur.objects.get(pk=uid_decoded)
    except (Utilisateur.DoesNotExist, ValueError, TypeError):
        return Response(
            {'error': 'Lien de réinitialisation invalide.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not default_token_generator.check_token(user, token):
        return Response(
            {'error': 'Token invalide ou expiré.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.set_password(new_password)
    user.save()
    
    return Response(
        {'message': 'Mot de passe réinitialisé avec succès.'},
        status=status.HTTP_200_OK
    )


# ==========================================
# SYSTEME DE POINTS ET RÉCOMPENSES
# ==========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mes_points(request):
    """Récupérer les points de l'utilisateur connecté"""
    utilisateur = request.user
    return Response({
        'points': utilisateur.points,
        'username': utilisateur.username,
        'peut_avoir_recompense': utilisateur.peut_avoir_recompense(),
        'points_restants': 100 - utilisateur.points if utilisateur.points < 100 else 0
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def historique_points(request):
    """Récupérer l'historique des transactions"""
    transactions = TransactionPoints.objects.filter(
        utilisateur=request.user
    ).order_by('-date_creation')
    
    data = [{
        'points': t.points,
        'type_transaction': t.get_type_transaction_display(),
        'description': t.description,
        'date_creation': t.date_creation
    } for t in transactions]
    
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reclamation_recompense(request):
    """Réclamer une récompense quand 100 points sont atteints"""
    utilisateur = request.user
    
    if utilisateur.points < 100:
        return Response({
            'error': f'Vous avez besoin de {100 - utilisateur.points} points supplémentaires.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Enlever 100 points
    utilisateur.ajouter_points(-100)
    
    TransactionPoints.objects.create(
        utilisateur=utilisateur,
        points=-100,
        type_transaction='bonus',
        description='Réclamation de récompense (100 points)'
    )
    
    return Response({
        'message': 'Félicitations ! Vous avez réclamé votre récompense de 100 points ! 🎉',
        'points_restants': utilisateur.points
    })