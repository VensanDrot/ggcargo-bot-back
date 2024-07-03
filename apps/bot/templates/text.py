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

reg_moderation_accept_uz = """
✅ Ваш аккаунт успешно зарегистрирован, удачных покупок!
Ваш ID: {customer_id}
"""
reg_moderation_accept_ru = """
✅ Sizning akkauntingiz muvaffaqiyatli ro‘yxatdan o‘tkazildi, omadli xaridlar!
Sizning ID: {customer_id}
"""
reg_moderation_decline_uz = """
❌ Вашему аккаунту было отказано!
Причина: {reject_message}
"""
reg_moderation_decline_ru = """
❌ Sizning akkauntingiz rad javob berildi!
Sabab: {reject_message}
"""
