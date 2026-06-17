from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Alerte Citoyenne",
      default_version='v1',
      description="Documentation API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('comptes.urls')),
    path('api/signalements/', include('signalements.urls')),
    path('api/messagerie/', include('messagerie.urls')),
    path('api/dons/', include('dons.urls')),
    path('api/moderation/', include('moderation.urls')),
    
    # ✅ Ajoutez la route Swagger ICI
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)