from rest_framework import serializers
from .models import Utilisateur, TransactionPoints

class InscriptionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = ['username', 'password', 'email', 'telephone', 'localisation', 'role']
        extra_kwargs = {
            'role': {'required': False},
            'email': {'required': False},
            'telephone': {'required': False},
            'localisation': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Utilisateur(**validated_data)
        user.set_password(password)
        user.save()
        
        # ==========================================
        # AJOUT : Points d'inscription
        # ==========================================
        user.ajouter_points(10)
        
        # Créer la transaction
        TransactionPoints.objects.create(
            utilisateur=user,
            points=10,
            type_transaction='inscription',
            description='Inscription sur CIVIALERT'
        )
        
        return user


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'telephone', 'localisation', 'role', 'points', 'date_inscription']
        read_only_fields = ['points', 'date_inscription']


class TransactionPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionPoints
        fields = ['id', 'points', 'type_transaction', 'description', 'date_creation']