from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Signalement
from .serializers import SignalementSerializer


class IsAuteurOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.auteur
            or request.user.role == 'admin'
            or request.user.role == 'moderateur'
        )


class SignalementViewSet(viewsets.ModelViewSet):
    queryset = Signalement.objects.all()
    serializer_class = SignalementSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)

    def get_queryset(self):
        queryset = Signalement.objects.all()
        type_alerte = self.request.query_params.get('type')
        statut = self.request.query_params.get('statut')
        if type_alerte:
            queryset = queryset.filter(type_alerte=type_alerte)
        if statut:
            queryset = queryset.filter(statut=statut)
        return queryset

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuteurOrAdmin]
        return super().get_permissions()
