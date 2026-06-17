from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Signalement
from .serializers import SignalementSerializer

class SignalementViewSet(viewsets.ModelViewSet):
    serializer_class = SignalementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Toutes les alertes pour tout le monde (fil d'actualité)
        return Signalement.objects.all().order_by('-date_soumission')

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        
        if 'statut' in request.data and user.role not in ['moderateur', 'admin']:
            return Response(
                {'error': 'Permission non accordée'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)