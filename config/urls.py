from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Cargo Swagger",
        default_version='v1',
        description="Swagger foy Cargo project, token authorization: user __/staff/token/__ API "
                    "then click authorize button and type __Bearer {token}__.",
        terms_of_service="https://google.com/",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="Cargo License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('control-panel/', admin.site.urls),
    path('bot/', include('apps.bot.urls')),
    path('staff/', include('apps.user.urls')),
    path('api/', include('apps.loads.urls')),
    path('tool/', include('apps.tools.urls')),
    path('file/', include('apps.files.urls')),
    path('payment/', include('apps.payment.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
