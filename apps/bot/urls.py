from django.urls import path

from apps.bot.views import BotWebhook

app_name = 'bot'
urlpatterns = [
    path('webhook/', BotWebhook.as_view())
]
