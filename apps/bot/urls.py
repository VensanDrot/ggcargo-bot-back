from django.urls import path

from apps.bot.views import AviaBotWebhook, AutoBotWebhook

app_name = 'bot'
urlpatterns = [
    path('webhook/avia/', AviaBotWebhook.as_view()),
    path('webhook/auto/', AutoBotWebhook.as_view())
]
