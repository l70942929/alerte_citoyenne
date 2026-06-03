from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonViewSet

router = DefaultRouter()
router.register(r'dons', DonViewSet, basename='don')

urlpatterns = [
    path('', include(router.urls)),
]