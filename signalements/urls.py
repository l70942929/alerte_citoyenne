from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_alertes, name='liste_alertes'),
    path('<int:id>/', views.detail_alerte, name='detail_alerte'),
    path('soumettre/', views.soumettre_alerte, name='soumettre_alerte'),
    path('moderer/<int:id>/', views.moderer_alerte, name='moderer_alerte'),
    path('supprimer/<int:id>/', views.supprimer_alerte, name='supprimer_alerte'),
    path('statistiques/', views.statistiques_alertes, name='statistiques_alertes'),
]