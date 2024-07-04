from telebot import types

from apps.bot.templates.text import location_button, ru_button, uz_button, reg_button


def location_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text=location_button, request_location=True)
    keyboard.add(button)
    return keyboard


def language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_uz = types.KeyboardButton(text=uz_button)
    button_ru = types.KeyboardButton(text=ru_button)
    keyboard.add(button_uz, button_ru)
    return keyboard


def reg_link_web_app_keyboard(web_app_link):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text=reg_button, web_app=web_app_link)
    keyboard.add(button)
    return keyboard
