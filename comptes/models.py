from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True, null=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)

    ROLE_CHOICES = [
        ('citoyen', 'Citoyen'),
        ('moderateur', 'Modérateur'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='citoyen'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateur_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateur_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} — {self.role}"