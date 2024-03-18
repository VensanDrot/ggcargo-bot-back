from telebot import types


def web_app_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    web_app = types.WebAppInfo("https://google.com")
    one_butt = types.KeyboardButton(text="Link To UI", web_app=web_app)
    keyboard.add(one_butt)

    return keyboard


def web_app_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    web_app = types.WebAppInfo("https://google.com")
    inline_button = types.InlineKeyboardButton(text="Link To UI", web_app=web_app)
    keyboard.add(inline_button)

    return keyboard
