from django.urls import path

from apps.tools.views import GetSettingsAPIView, PostSettingsAPIView, NewsletterListAPIView, NewsletterCreateAPIView, \
    NewsletterUpdateAPIView, NewsletterRetrieveAPIView

app_name = 'tool'
urlpatterns = [
    path('get-settings/', GetSettingsAPIView.as_view(), name='get_settings'),
    path('post-settings/', PostSettingsAPIView.as_view(), name='post_settings'),
    path('newsletter/list/', NewsletterListAPIView.as_view(), name='newsletter_list'),
    path('newsletter/create/', NewsletterCreateAPIView.as_view(), name='newsletter_create'),
    path('newsletter/update/<int:pk>/', NewsletterUpdateAPIView.as_view(), name='newsletter_update'),
    path('newsletter/retrieve/<int:pk>/', NewsletterRetrieveAPIView.as_view(), name='newsletter_retrieve'),
]
