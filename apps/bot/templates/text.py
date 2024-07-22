delivery_text = """
<b>Заявка на отправку!</b> [{date}]

ID: {customer_id}
Вес: {weight} kg.

Способ доставки: {delivery_type}
Номер телефона: {phone_number}
Комментарий: {comment}

{track_link}
"""
request_location = "Для того, чтобы наш оператор мог отправить ваш груз, пожалуйста отправьте вашу геолокацию!"
success_location = "✅ Спасибо, ваша заявка оформлена!"
mail_success = """
✅ Спасибо, ваша заявка оформлена!

Трекинг линк: {track_link}
"""
location_button = "📍 Отправить локацию"
uz_button = "Oʻzbekcha 🇺🇿"
ru_button = "Русский 🇷🇺"
reg_button_uz = "«Ro’yxatdan o’tish»"
reg_button_ru = "«Начать регистрацию»"
reg_button_uz_ru = "«Ro’yxatdan o’tish»/«Начать регистрацию»"
instruction_ru = "Перед регистрацией, пожалуйста ознакомьтесь с инструкцией по работе с нашим мобильным приложением. Удачных покупок 🚀"
instruction_uz = "Ro'yxatdan o'tishdan oldin, iltimos, bizning mobil ilovamiz bilan ishlash bo'yicha qo'llanmani ko'rib chiqing. Muvaffaqiyatli xaridlar tilaymiz 🚀"

reg_moderation_accept_ru = """
✅ Ваш аккаунт успешно зарегистрирован, удачных покупок\!
Ваш ID:
{customer_id}
"""
reg_moderation_accept_uz = """
✅ Sizning akkauntingiz muvaffaqiyatli ro‘yxatdan o‘tkazildi, omadli xaridlar\!
Sizning ID:
{customer_id}

"""
customer_menu_instruction_uz = """
Siz ro’yxatdan o’tdingiz! Keyingi qadamingiz qanday?

Botdan qanday foydalanishni bilib olish uchun ushbu videoni ko’ring.
"""
customer_menu_instruction_ru = """
Вот вы и зарегистрировались! Что делать дальше?

Чтобы узнать, как пользоваться нашим ботом, посмотрите это видео.
"""
reg_moderation_decline_ru = """
❌ Вашему аккаунту было отказано!
Причина: {reject_message}
"""
reg_moderation_decline_uz = """
❌ Sizning akkauntingiz rad javob berildi!
Sabab: {reject_message}
"""
welcome_bot_message = "Добро пожаловать в Express Cargo! Пожалуйста выберите язык 🇺🇿🇷🇺"
after_start_message = """
Для того, чтобы открыть мобильное приложение еще раз, нажмите на кнопку под этим сообщением, или воспользуйтесь кнопкой "Меню" в приборной панели бота 📲
———
Mobil ilovani yana bir bor ochish uchun ushbu xabarning ostidagi tugmani bosing yoki botning boshqaruv panelidagi "Menyu" tugmasidan foydalaning 📲
"""
copy_text_uz = "Nusxa ko'chirish"
copy_text_ru = "Копировать"
