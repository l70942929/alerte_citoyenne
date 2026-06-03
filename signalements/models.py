from django.db import models
from django.conf import settings

class Signalement(models.Model):

    TYPE_CHOICES = [
        ('kidnapping', 'Kidnapping'),
        ('disparition', 'Disparition'),
        ('perte_objet', "Perte d'objet"),
        ('decouverte', 'Découverte'),
        ('accident', 'Accident'),
    ]

    STATUT_CHOICES = [
        ('recu', 'Reçu'),
        ('en_cours', 'En cours'),
        ('resolu', 'Résolu'),
        ('cloture', 'Clôturé'),
    ]

    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='signalements'
    )
    type_alerte = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    localisation = models.CharField(max_length=255)
    date_evenement = models.DateTimeField()
    date_soumission = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(
        upload_to='photos/', blank=True, null=True
    )
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default='recu'
    )
    anonyme = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type_alerte} - {self.localisation}"

    class Meta:
        ordering = ['-date_soumission']
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'


# ← ICI en dehors de Signalement
class Notification(models.Model):

    TYPE_CHOICES = [
        ('push', 'Push'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    contenu = models.TextField()
    type_notif = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default='push'
    )
    lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)
    signalement = models.ForeignKey(
        Signalement,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='notifications'
    )

    def __str__(self):
        return f"Notif → {self.utilisateur.username}"

    class Meta:
        ordering = ['-date_envoi']