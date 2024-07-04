from telebot import types, TeleBot

from apps.bot.templates.text import uz_button, ru_button
from apps.bot.utils.keyboards import reg_link_web_app_keyboard


def language_handler(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    handler_tool[message.text](message, bot, web_app_link)


def send_uz_instruction(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    instruction_url = 'https://backend.gogocargo.uz/media/uploads/instruction_uz.MP4'
    bot.send_video(message.chat.id, instruction_url, reply_markup=reg_link_web_app_keyboard(web_app_link))


def send_ru_instruction(message: types.Message, bot: TeleBot, web_app_link: str) -> None:
    instruction_url = 'https://backend.gogocargo.uz/media/uploads/instruction_ru.MP4'
    bot.send_video(message.chat.id, instruction_url, reply_markup=reg_link_web_app_keyboard(web_app_link))


handler_tool = {
    uz_button: send_uz_instruction,
    ru_button: send_ru_instruction
}
