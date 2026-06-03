from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('comptes.urls')),
    path('api/signalements/', include('signalements.urls')),
    path('api/messagerie/', include('messagerie.urls')),
    path('api/dons/', include('dons.urls')),
    path('api/moderation/', include('moderation.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)