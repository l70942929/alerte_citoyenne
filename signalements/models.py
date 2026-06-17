from django.db import models
from django.conf import settings

class Signalement(models.Model):
    TYPE_CHOICES = [
        ('kidnapping', 'Kidnapping'),
        ('disparition', 'Disparition'),
        ('perte_objet', 'Perte d\'objet'),
        ('decouverte', 'Découverte'),
        ('accident', 'Accident'),
    ]
    
    STATUT_CHOICES = [
        ('recu', 'Reçu'),
        ('en_cours', 'En cours de traitement'),
        ('resolu', 'Résolu'),
        ('cloture', 'Clôturé'),
    ]
    
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='signalements'
    )
    type_alerte = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField()
    localisation = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    date_evenement = models.DateTimeField()
    date_soumission = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    anonyme = models.BooleanField(default=False)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='recu')
    
    def __str__(self):
        return f"{self.get_type_alerte_display()} - {self.localisation} - {self.utilisateur.username}"