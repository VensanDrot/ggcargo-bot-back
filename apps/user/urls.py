from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.views import UserModelViewSet, AdminJWTObtainPairView, CustomerJWTObtainPairView

router = DefaultRouter()
router.register('users', UserModelViewSet, basename='users')

app_name = 'staff'
urlpatterns = [
    path('admin/token/', AdminJWTObtainPairView.as_view(), name='admin_token_obtain_pair'),
    path('customer/token/', CustomerJWTObtainPairView.as_view(), name='customer_token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('create/', .as_view(), name='user_create'),
]
urlpatterns += router.urls
