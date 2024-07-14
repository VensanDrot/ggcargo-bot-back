import logging
from os.path import join as join_path

from django.conf import settings
from telebot import types, TeleBot

from apps.bot.templates.text import uz_button, ru_button, instruction_uz, instruction_ru
from apps.bot.utils.keyboards import reg_link_web_app_keyboard

logger = logging.getLogger()


def language_handler(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    handler_tool[message.text](message, bot, web_app_link)


def send_uz_instruction(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    file_path = join_path(settings.MEDIA_ROOT, 'instructions', "Qõllanma.mp4")
    with open(file_path, 'rb') as video:
        loader = bot.send_message(chat_id=message.chat.id, text='Fayl yuborilyabdi...',
                                  reply_markup=types.ReplyKeyboardRemove())
        # bot.send_video(chat_id=message.chat.id, video=video, supports_streaming=False ,
        #                reply_markup=reg_link_web_app_keyboard(web_app_link, 'uz'))
        try:
            bot.send_document(chat_id=message.chat.id, document=video, caption=instruction_uz,
                              reply_markup=reg_link_web_app_keyboard(web_app_link, 'uz'))
        except Exception as exc:
            logger.debug(f'Error occurred: {exc.args}')
    bot.delete_message(chat_id=message.chat.id, message_id=loader.message_id)


def send_ru_instruction(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    file_path = join_path(settings.MEDIA_ROOT, 'instructions', 'Руководство.mp4')
    with open(file_path, 'rb') as video:
        loader = bot.send_message(chat_id=message.chat.id, text='Файл отправляется...',
                                  reply_markup=types.ReplyKeyboardRemove())
        # bot.send_video(chat_id=message.chat.id, video=video, supports_streaming=False ,
        #                reply_markup=reg_link_web_app_keyboard(web_app_link, 'ru'))
        try:
            bot.send_document(chat_id=message.chat.id, document=video, caption=instruction_ru,
                              reply_markup=reg_link_web_app_keyboard(web_app_link, 'ru'))
        except Exception as exc:
            logger.debug(f'Error occurred: {exc.args}')
    bot.delete_message(chat_id=message.chat.id, message_id=loader.message_id)


handler_tool = {
    uz_button: send_uz_instruction,
    ru_button: send_ru_instruction
}
