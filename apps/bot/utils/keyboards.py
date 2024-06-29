from telebot import types

from apps.bot.templates.text import location_button


def location_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text=location_button, request_location=True)
    keyboard.add(button)
    return keyboard
