from rest_framework import serializers
from .models import Utilisateur

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
        return user

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'telephone', 'localisation', 'role']