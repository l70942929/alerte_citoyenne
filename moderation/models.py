# Create your models here.
from django.db import models
from django.conf import settings
from signalements.models import Signalement

class Moderation(models.Model):

    DECISION_CHOICES = [
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
        ('complement', 'Complément demandé'),
    ]

    signalement = models.ForeignKey(
        Signalement, on_delete=models.CASCADE,
        related_name='moderations'
    )
    moderateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='moderations'
    )
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES)
    motif = models.TextField(blank=True, null=True)
    date_decision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.decision} - {self.signalement}"

    class Meta:
        ordering = ['-date_decision']