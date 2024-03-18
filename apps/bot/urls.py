from django.urls import path

from apps.bot.views import CargoBotWebhook

app_name = 'bot'
urlpatterns = [
    path('bot/webhook/', CargoBotWebhook.as_view())
]
