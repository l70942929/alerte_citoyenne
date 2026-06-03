from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Moderation
from .serializers import ModerationSerializer
from signalements.models import Signalement

class ModerationViewSet(viewsets.ModelViewSet):
    queryset = Moderation.objects.all()
    serializer_class = ModerationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        moderation = serializer.save(moderateur=self.request.user)
        # Mettre à jour le statut du signalement
        signalement = moderation.signalement
        if moderation.decision == 'valide':
            signalement.statut = 'en_cours'
        elif moderation.decision == 'rejete':
            signalement.statut = 'cloture'
        signalement.save()

    @action(detail=False, methods=['get'])
    def en_attente(self, request):
        alertes = Signalement.objects.filter(statut='recu')
        from signalements.serializers import SignalementSerializer
        serializer = SignalementSerializer(alertes, many=True)
        return Response(serializer.data)