from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    
    # Mot de passe oublié
    path('mot-de-passe-oublie/', views.mot_de_passe_oublie, name='mot_de_passe_oublie'),
    path('reinitialiser-mot-de-passe/', views.reinitialiser_mot_de_passe, name='reinitialiser_mot_de_passe'),
    
    # Système de points
    path('mes-points/', views.mes_points, name='mes_points'),
    path('historique-points/', views.historique_points, name='historique_points'),
    path('reclamation-recompense/', views.reclamation_recompense, name='reclamation_recompense'),
]