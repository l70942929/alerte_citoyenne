# Create your models here.
from django.db import models
from django.conf import settings

class Don(models.Model):

    MOYEN_CHOICES = [
        ('mtn', 'MTN Mobile Money'),
        ('orange', 'Orange Money'),
        ('carte', 'Carte bancaire'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('echoue', 'Échoué'),
    ]

    donateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='dons'
    )
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    moyen = models.CharField(max_length=20, choices=MOYEN_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.donateur} - {self.montant} FCFA"

    class Meta:
        ordering = ['-date']