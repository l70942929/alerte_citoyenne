from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Don
from .serializers import DonSerializer

class DonViewSet(viewsets.ModelViewSet):
    serializer_class = DonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Don.objects.filter(donateur=self.request.user)

    def perform_create(self, serializer):
        serializer.save(donateur=self.request.user)

    @action(detail=True, methods=['post'])
    def confirmer(self, request, pk=None):
        don = self.get_object()
        don.statut = 'confirme'
        don.save()
        return Response({'message': 'Don confirmé avec succès'})