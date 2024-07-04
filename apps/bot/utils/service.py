from os.path import join as join_path

from django.conf import settings
from telebot import types, TeleBot

from apps.bot.templates.text import uz_button, ru_button
from apps.bot.utils.keyboards import reg_link_web_app_keyboard


def language_handler(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    handler_tool[message.text](message, bot, web_app_link)


def send_uz_instruction(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    file_id = 'BAACAgIAAxkBAAIFy2aGQZH9ijbWsV2bL3d30fui-sDAAAISSAACuzkwSAebLL3Tv_yzNQQ'
    file_url = 'https://backend.gogocargo.uz/media/instructions/instruction_uz.MP4'
    # file_path = join_path(settings.MEDIA_ROOT, 'instructions', 'instruction_uz.MP4')
    # with open(file_path, 'rb') as video:
    # bot.send_video(chat_id=message.chat.id, video=file_id, supports_streaming=True,
    #                reply_markup=reg_link_web_app_keyboard(web_app_link, 'uz'))
    bot.send_document(chat_id=message.chat.id, document=file_url,
                      reply_markup=reg_link_web_app_keyboard(web_app_link, 'uz'))
    remover = bot.send_message(chat_id=message.chat.id, text='.', reply_markup=types.ReplyKeyboardRemove())
    bot.delete_message(chat_id=message.chat.id, message_id=remover.message_id)


def send_ru_instruction(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    file_id = 'BAACAgIAAxkBAAIFzGaGQdG8NUdHrxOizmhpOa6c-Kp1AAIUSAACuzkwSBMp2bWO3gdUNQQ'
    # file_path = join_path(settings.MEDIA_ROOT, 'instructions', 'instruction_ru.MP4')
    # with open(file_path, 'rb') as video:
    bot.send_video(chat_id=message.chat.id, video=file_id, supports_streaming=True,
                   reply_markup=reg_link_web_app_keyboard(web_app_link, 'ru'))
    remover = bot.send_message(chat_id=message.chat.id, text='.', reply_markup=types.ReplyKeyboardRemove())
    bot.delete_message(chat_id=message.chat.id, message_id=remover.message_id)


handler_tool = {
    uz_button: send_uz_instruction,
    ru_button: send_ru_instruction
}