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
