import logging
from os.path import join as join_path

from django.conf import settings
from telebot import types, TeleBot

from apps.bot.templates.text import uz_button, ru_button, instruction_uz, instruction_ru
from apps.bot.utils.keyboards import reg_link_web_app_keyboard
from apps.bot.utils.tools import send_instruction

logger = logging.getLogger()


def language_handler(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    handler_tool[message.text](message, bot, web_app_link)


def send_uz_instruction(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    send_instruction(message, bot, caption=instruction_uz, file_name="Qõllanma.mp4",
                     keyboard=reg_link_web_app_keyboard(web_app_link, 'uz'), loader_text="Fayl yuborilyabdi...")


def send_ru_instruction(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    send_instruction(message, bot, caption=instruction_ru, file_name="Руководство.mp4",
                     keyboard=reg_link_web_app_keyboard(web_app_link, 'ru'), loader_text="Файл отправляется...")


handler_tool = {
    uz_button: send_uz_instruction,
    ru_button: send_ru_instruction
}
