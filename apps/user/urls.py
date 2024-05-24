from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.routes.web import UserModelViewSet, CustomerModelViewSet, CustomerIDPrefix
from apps.user.routes.telegram import CustomerAviaRegistrationStepOneAPIView, CustomerAviaRegistrationStepTwoAPIView, \
    CustomerAviaRegistrationStepThreeAPIView, CustomerAutoRegistrationStepOneAPIView, \
    CustomerAutoRegistrationStepTwoAPIView, CustomerSettingsPersonalUpdateAPIView, \
    CustomerSettingsPersonalRetrieveAPIView, CustomerSettingsPasswordUpdateAPIView
from apps.user.views import JWTObtainPairView, TelegramLoginAPIView

router = DefaultRouter()
router.register('users', UserModelViewSet, basename='users')
router.register('customers', CustomerModelViewSet, basename='customers')

app_name = 'staff'
urlpatterns = [
    path('token/', JWTObtainPairView.as_view(), name='admin_token_obtain_pair'),
    path('telegram/token/', TelegramLoginAPIView.as_view(), name='telegram_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customer-id/prefix-list/<str:user_type>/', CustomerIDPrefix.as_view(), name='token_refresh'),

    path('customer/avia/registration/step-one/', CustomerAviaRegistrationStepOneAPIView.as_view(),
         name='customer_avia_registration_step_one'),
    path('customer/avia/registration/step-two/<int:pk>/', CustomerAviaRegistrationStepTwoAPIView.as_view(),
         name='customer_avia_registration_step_two'),
    path('customer/avia/registration/step-three/<int:pk>/', CustomerAviaRegistrationStepThreeAPIView.as_view(),
         name='customer_avia_registration_step_three'),
    path('customer/auto/registration/step-one/', CustomerAutoRegistrationStepOneAPIView.as_view(),
         name='customer_auto_registration_step_one'),
    path('customer/auto/registration/step-two/<int:pk>/', CustomerAutoRegistrationStepTwoAPIView.as_view(),
         name='customer_auto_registration_step_two'),

    path('customer/settings/personal/retrieve/', CustomerSettingsPersonalRetrieveAPIView.as_view(),
         name='customer_settings_personal_retrieve'),
    path('customer/settings/personal/update/', CustomerSettingsPersonalUpdateAPIView.as_view(),
         name='customer_settings_personal_update'),
    path('customer/settings/password/update/', CustomerSettingsPasswordUpdateAPIView.as_view(),
         name='customer_settings_password_update'),
]
urlpatterns += router.urls
