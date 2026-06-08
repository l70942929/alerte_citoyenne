from email.mime import message

from rest_framework import request, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(expediteur=user) | Q(destinataire=user)
        )
    def destroy(self, request, *args, **kwargs):
        message = self.get_object()

        if message.expediteur != request.user:
          return Response(
            {"erreur": "Action non autorisée"},
            status=403
        )

        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(expediteur=self.request.user)

    @action(detail=False, methods=['get'])
    def conversation(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'erreur': 'user_id requis'}, status=400)
        user = request.user
        messages = Message.objects.filter(
            Q(expediteur=user, destinataire_id=user_id) |
            Q(expediteur_id=user_id, destinataire=user)
        ).order_by('date_envoi')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)