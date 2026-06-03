from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModerationViewSet

router = DefaultRouter()
router.register(r'moderations', ModerationViewSet, basename='moderation')

urlpatterns = [
    path('', include(router.urls)),
]