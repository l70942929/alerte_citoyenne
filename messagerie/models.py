from django.db import models
from django.conf import settings
from signalements.models import Signalement

class Message(models.Model):
    expediteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_envoyes'
    )
    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_recus'
    )
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    signalement = models.ForeignKey(
        Signalement,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='messages'
    )

    def __str__(self):
        return f"{self.expediteur} → {self.destinataire}"

    class Meta:
        ordering = ['date_envoi']