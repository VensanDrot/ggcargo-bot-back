from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.views import UserModelViewSet, JWTObtainPairView, CustomerModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet, basename='users')
router.register('customers', CustomerModelViewSet, basename='customers')

app_name = 'staff'
urlpatterns = [
    path('token/', JWTObtainPairView.as_view(), name='admin_token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += router.urls
