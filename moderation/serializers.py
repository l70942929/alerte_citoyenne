from rest_framework import serializers
from .models import Moderation

class ModerationSerializer(serializers.ModelSerializer):
    moderateur_nom = serializers.CharField(
        source='moderateur.username', read_only=True
    )
    class Meta:
        model = Moderation
        fields = '__all__'
        read_only_fields = ['moderateur', 'date_decision']