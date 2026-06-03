from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Signalement

class SignalementSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.CharField(
        source='auteur.username', read_only=True
    )
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Signalement
        fields = '__all__'
        read_only_fields = ['auteur', 'date_soumission', 'statut']

    def validate(self, attrs):
        if self.instance is None and not attrs.get('photo'):
            raise ValidationError({'photo': 'Une photo est requise pour signaler une alerte.'})
        return super().validate(attrs)
