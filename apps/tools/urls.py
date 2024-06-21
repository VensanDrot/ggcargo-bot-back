from django.urls import path

from apps.tools.views import GetSettingsAPIView, PostSettingsAPIView, NewsletterListAPIView, NewsletterCreateAPIView, \
    NewsletterUpdateAPIView, NewsletterRetrieveAPIView, FourthDashboardAPIView, FirstDashboardAPIView, \
    SecondDashboardAPIView, ThirdDashboardAPIView, FifthDashboardAPIView

app_name = 'tool'
urlpatterns = [
    path('get-settings/', GetSettingsAPIView.as_view(), name='get_settings'),
    path('post-settings/', PostSettingsAPIView.as_view(), name='post_settings'),
    path('newsletter/list/', NewsletterListAPIView.as_view(), name='newsletter_list'),
    path('newsletter/create/', NewsletterCreateAPIView.as_view(), name='newsletter_create'),
    path('newsletter/update/<int:pk>/', NewsletterUpdateAPIView.as_view(), name='newsletter_update'),
    path('newsletter/retrieve/<int:pk>/', NewsletterRetrieveAPIView.as_view(), name='newsletter_retrieve'),

    # Dashboard
    path('admin/dashboard/first-chart/', FirstDashboardAPIView.as_view(), name='dashboard_first'),
    path('admin/dashboard/second-chart/', SecondDashboardAPIView.as_view(), name='dashboard_second'),
    path('admin/dashboard/third-chart/', ThirdDashboardAPIView.as_view(), name='dashboard_third'),
    path('admin/dashboard/fourth-chart/', FourthDashboardAPIView.as_view(), name='dashboard_fourth'),
    path('admin/dashboard/fifth-chart/', FifthDashboardAPIView.as_view(), name='dashboard_fifth'),
]
