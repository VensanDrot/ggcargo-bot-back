import logging

from django.conf import settings
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot import TeleBot, types
from telebot.types import Update, ReplyKeyboardRemove

from apps.bot.templates.text import success_location, welcome_bot_message, after_start_message
from apps.bot.utils.keyboards import language_keyboard, web_app_keyboard
from apps.bot.utils.service import language_handler
from apps.user.models import Customer

logger = logging.getLogger()
bot_tokens = settings.BOT_TOKENS

avia_customer_bot = TeleBot(bot_tokens['avia_customer'])
auto_customer_bot = TeleBot(bot_tokens['auto_customer'])

user_states = {}


class AviaBotWebhook(APIView):
    permission_classes = [AllowAny, ]

    @staticmethod
    def post(request):
        update = Update.de_json(request.data)
        avia_customer_bot.process_new_updates([update])
        return Response({'message': 'Success!',
                         'status': status.HTTP_200_OK})


class AutoBotWebhook(APIView):
    permission_classes = [AllowAny, ]

    @staticmethod
    def post(request):
        update = Update.de_json(request.data)
        auto_customer_bot.process_new_updates([update])
        return Response({'message': 'Success!',
                         'status': status.HTTP_200_OK})


@avia_customer_bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.from_user.id
    if chat_id not in user_states:
        welcome_bot = welcome_bot_message
        avia_customer_bot.send_message(chat_id=message.from_user.id, text=welcome_bot, reply_markup=language_keyboard())
        user_states[message.from_user.id] = 'started'
    else:
        avia_customer_bot.send_message(chat_id=message.from_user.id, text=after_start_message,
                                       reply_markup=web_app_keyboard('https://avia.gogocargo.uz'))


@auto_customer_bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.from_user.id
    if chat_id not in user_states:
        welcome_bot = welcome_bot_message
        auto_customer_bot.send_message(chat_id=message.from_user.id, text=welcome_bot, reply_markup=language_keyboard())
        user_states[message.from_user.id] = 'started'
    else:
        auto_customer_bot.send_message(chat_id=message.from_user.id, text=after_start_message,
                                       reply_markup=web_app_keyboard('https://auto.gogocargo.uz'))


@avia_customer_bot.message_handler(content_types=['text'])
def handle_message(message: types.Message):
    language_handler(message, avia_customer_bot, 'https://avia.gogocargo.uz')


@auto_customer_bot.message_handler(content_types=['text'])
def handle_message(message: types.Message):
    language_handler(message, auto_customer_bot, 'https://auto.gogocargo.uz')


@avia_customer_bot.message_handler(content_types=['location'])
def handle_content_avia(message: types.Message):
    try:
        tg_id = message.chat.id
        customer = get_object_or_404(Customer, tg_id=tg_id, user_type='AVIA')
        location = message.location.to_dict()
        customer.location = location
        customer.save()
        delivery = customer.deliveries.filter(message_sent=False).order_by('-id').first()
        if delivery:
            avia_customer_bot.send_message(chat_id=tg_id, text=success_location, reply_markup=ReplyKeyboardRemove())
            avia_customer_bot.send_location(chat_id=-1002187675934, reply_to_message_id=delivery.telegram_message_id,
                                            latitude=location['latitude'], longitude=location['longitude'])
    except Exception as exc:
        logger.debug(f'Telegram AVIA location_handler error occurred: {exc.args}')


@auto_customer_bot.message_handler(content_types=['location'])
def handle_content_auto(message: types.Message):
    try:
        tg_id = message.chat.id
        customer = get_object_or_404(Customer, tg_id=tg_id, user_type='AUTO')
        location = message.location.to_dict()
        customer.location = location
        customer.save()
        delivery = customer.deliveries.filter(message_sent=False).order_by('-id').first()
        if delivery:
            auto_customer_bot.send_message(chat_id=tg_id, text=success_location, reply_markup=ReplyKeyboardRemove())
            auto_customer_bot.send_location(chat_id=-1002187675934, reply_to_message_id=delivery.telegram_message_id,
                                            latitude=location['latitude'], longitude=location['longitude'])
    except Exception as exc:
        logger.debug(f'Telegram AUTO location_handler error occurred: {exc.args}')
