# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Utilisateur
from .serializers import InscriptionSerializer, UtilisateurSerializer

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
            'role': user.role
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
            'role': user.role
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