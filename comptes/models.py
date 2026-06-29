from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('citoyen', 'Citoyen'),
        ('moderateur', 'Modérateur'),
        ('admin', 'Administrateur'),
    ]
    
    telephone = models.CharField(max_length=20, blank=True, null=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citoyen')
    points = models.IntegerField(default=0)  # <-- NOUVEAU : Points de l'utilisateur
    date_inscription = models.DateTimeField(auto_now_add=True)  # <-- NOUVEAU
    
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
    
    # ==========================================
    # METHODES POUR LES POINTS
    # ==========================================
    
    def ajouter_points(self, points):
        """Ajouter des points à l'utilisateur"""
        self.points += points
        self.save()
        return self.points
    
    def peut_avoir_recompense(self):
        """Vérifier si l'utilisateur peut avoir une récompense (100 points)"""
        return self.points >= 100


# ==========================================
# MODELE TRANSACTION POINTS
# ==========================================

class TransactionPoints(models.Model):
    TYPE_CHOICES = (
        ('inscription', 'Inscription'),
        ('soumission', 'Soumission d\'alerte'),
        ('verification', 'Alerte vérifiée'),
        ('resolution', 'Alerte résolue'),
        ('retrouve', 'Objet/personne retrouvé(e)'),
        ('bonus', 'Bonus'),
    )
    
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='transactions')
    points = models.IntegerField()
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.points} pts ({self.type_transaction})"