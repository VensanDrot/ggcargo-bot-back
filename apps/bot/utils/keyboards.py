from telebot import types
from telebot.types import WebAppInfo

from apps.bot.templates.text import location_button, ru_button, uz_button, reg_button_uz, reg_button_ru, \
    reg_button_uz_ru


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


def reg_link_web_app_keyboard(web_app_link, lang, button_text=None):
    keyboard = types.InlineKeyboardMarkup()
    web_app_info = WebAppInfo(url=web_app_link)
    if not button_text:
        button_text = reg_button_uz if lang == 'uz' else reg_button_ru
    else:
        button_text = '«Ilovani ochish»' if lang == 'uz' else '«Открыть приложение»'
    button = types.InlineKeyboardButton(text=button_text, web_app=web_app_info)
    keyboard.add(button)
    return keyboard


def web_app_keyboard(web_app_link):
    keyboard = types.InlineKeyboardMarkup()
    web_app_info = WebAppInfo(url=web_app_link)
    button = types.InlineKeyboardButton(text=reg_button_uz_ru, web_app=web_app_info)
    keyboard.add(button)
    return keyboard
