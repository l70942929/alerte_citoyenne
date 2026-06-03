from rest_framework import serializers
from .models import Don

class DonSerializer(serializers.ModelSerializer):
    donateur_nom = serializers.CharField(
        source='donateur.username', read_only=True
    )
    class Meta:
        model = Don
        fields = '__all__'
        read_only_fields = ['donateur', 'date', 'statut']