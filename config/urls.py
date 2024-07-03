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


Customer endpoints: startswith __/api/customer/.../__ | __/payment/customer/.../__ | __/staff/customer/...__
/api/customer/current-load/ for page __Мои загрузки (Текущая)__ 
/api/customer/own-loads/history/ for page __Мои загрузки (История загрузок)__
/payment/customer/load-payment/ for page __Оплата (скриншот с оплатой на модерацию)__

Customer AUTO Registrations: STEP-1 __/staff/customer/auto/registration/step-one/__, STEP-2 __/staff/customer/auto/registration/step-two/{id}/__
Customer AVIA Registrations: STEP-1 __/staff/customer/avia/registration/step-one/__, STEP-2 __/staff/customer/avia/registration/step-two/{id}/__, STEP-3: __/staff/customer/avia/registration/step-three/{id}/__
<id>-provided in url's path is which returned in STEP-1 

<br>
<h4>UPDATES 2024-05-26</h4>
Customer Statistics:
__/staff/customer/stats/__  статистика кастомера

Customer Настройки (Personal data):
__/staff/customer/settings/personal/retrieve/__ to get personal data
__/staff/customer/settings/personal/update/__ to change personal data
__/staff/customer/settings/password/update/__ to change password

Customer Найти груз вручную:
__/api/customer/track/product/<str:barcode>/__ for page __Отслеживание посылки__


Customer Получить груз:
__/payment/customer/delivery/__ to send request for a delivery

Customer Посылки В пути:
__/api/customer/products-on-way/list/__ to get list of products on the way


Web Admin Newsletter:
__newsletter/list/__  to get list of newsletters
__newsletter/create/__  to create newsletter
__newsletter/update/<int:pk>/__  to update newsletter
__newsletter/retrieve/<int:pk>/__  to retrieve newsletter


Settings info for Customers:
__/staff/customer/payment-card/__ to get payment card
__/staff/customer/take-away-address/__ to get company address
__/staff/customer/footer/__ to get company address, channel link and support information


Moderation of Customer's registrations:
__/staff/customer-moderation/list/__ to get list of registration applications
__/staff/customer-moderation/retrieve/{id}/__ to retrieve registration application | get {id} from url /list/ endpoint
__/staff/customer-moderation/accept/{id}/__ to accept registration application
__/staff/customer-moderation/decline/{id}/__ to decline registration application

<br>
<h4>UPDATES 2024-06-21</h4>
Analytics dashboard data:
__/tool/admin/dashboard/first-chart/__  -  first chart
__/tool/admin/dashboard/second-chart/__  -  second chart
__/tool/admin/dashboard/third-chart/__  -  third chart
__/tool/admin/dashboard/fourth-chart/__  -  fourth chart
__/tool/admin/dashboard/fifth-chart/__  -  fifth chart

<br>
<h4>UPDATES 2024-06-24</h4>
Open API to check barcode's status:
__/api/open/product/{barcode}/__

<br>
<h4>UPDATES 2024-07-03</h4>
EMU Regions and Districts list:
__/integration/emu/regions/__  to get list of regions
__/integration/emu/districts/{region}/__  pass region name to get list of districts

__/payment/customer/delivery/__  endpoint updated: added MAIL delivery type. Json request body example:
```
{
  "delivery_type": "MAIL",
  "phone_number": "+998901112233",
  "town": 143,  # pass district id which you get from district's list
  "address": "Новза махалля, 15-22",
  "service_type": 3,  # 1 or 3. 1=От офиса до офиса, 3=На руки получателю
  "comment": "Позвоните заранее перед приездом"
}
```
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
    path('integration/', include('apps.integrations.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
