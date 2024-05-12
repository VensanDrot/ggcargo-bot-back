from django.urls import path

from apps.tools.views import GetSettingsAPIView, PostSettingsAPIView

app_name = 'tool'
urlpatterns = [
    path('get-settings/', GetSettingsAPIView.as_view(), name='get_settings'),
    path('post-settings/', PostSettingsAPIView.as_view(), name='post_settings'),
]
