from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot import TeleBot, types
from telebot.types import Update

from apps.bot.utils.keyboards import web_app_keyboard, web_app_inline_keyboard

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
    delete_text = bot.send_message(chat_id=message.from_user.id, text='Loading...',
                                   reply_markup=types.ReplyKeyboardRemove())
    bot.delete_message(chat_id=message.from_user.id, message_id=delete_text.message_id)
    bot.send_message(chat_id=message.from_user.id, text="Salom", reply_markup=web_app_inline_keyboard())


@bot.message_handler(content_types=['text'])
def handle_message(message: types.Message):
    bot.send_message(chat_id=message.from_user.id, text=message.text, reply_markup=web_app_keyboard())
