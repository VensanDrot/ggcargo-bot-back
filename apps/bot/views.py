from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot import TeleBot, types
from telebot.types import Update

bot = TeleBot(settings.BOT_TOKEN)


class CargoBotWebhook(APIView):

    @staticmethod
    def post(request):
        update = Update.de_json(request.data)
        bot.process_new_updates([update])
        return Response({'message': 'Success!',
                         'status': status.HTTP_200_OK})


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(chat_id=message.from_user.id, text="Hello World!")
