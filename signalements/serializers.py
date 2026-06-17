from rest_framework import serializers
from .models import Signalement

class SignalementSerializer(serializers.ModelSerializer):
    utilisateur_nom = serializers.CharField(source='utilisateur.username', read_only=True)
    
    class Meta:
        model = Signalement
        fields = '__all__'
        read_only_fields = ['utilisateur', 'date_soumission']