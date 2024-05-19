from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

swagger_description = """
__Authorization: Bearer <ACCESS_TOKEN>__, Get tokens from __/staff/token/__ and __/staff/telegram/token/__

Web Operator endpoints:
/api/admin/delivery/.../ for page __Посылки__
/api/admin/loads/.../ for page __Загрузки__
/payment/admin/.../ for page __Модерация/Payments__

Tashkent Telegram Operator endpoints: startswith __/api/operator/tashkent/.../__,
/api/operator/tashkent/moderation/.../ for page __Модерация__
/api/operator/tashkent/release/.../ for page __Выдать Груз__


Customer endpoints: startswith __/api/customer/.../__ and __/payment/customer/.../__
/api/customer/current-load/, /api/customer/own-loads/history/ for page __My Loads__
/payment/customer/load-payment/ for page __Payment__
"""

schema_view = get_schema_view(
    openapi.Info(
        title="Cargo Swagger",
        default_version='v1',
        description=swagger_description,
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
