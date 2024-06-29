from django.utils.translation import gettext_lazy as _

# CUSTOMERS
AUTO = 'AUTO'
AVIA = 'AVIA'
CAR_OR_AIR_CHOICE = [
    (AUTO, _('Auto')),
    (AVIA, _('Avia'))
]
GG = 'GG'
EXP = 'EXP'
CHINA = 'CHINA'
COMPANY_TYPE_CHOICES = [
    (GG, GG),
    (EXP, EXP),
    (CHINA, CHINA),
]

WSC = 'WSC'
YDQ = 'YDQ'
ZRD = 'ZRD'
HVP = 'HVP'
LXE = 'LXE'
GZG = 'GZG'
DELETE = 'DELETE'
PREFIX_CHOICES = [
    (WSC, 'WSC'),
    (YDQ, 'YDQ'),
    (ZRD, 'ZRD'),
    (HVP, 'HVP'),
    (LXE, 'LXE'),
    (GZG, 'GZG'),
    (DELETE, 'DELETE'),
]

WAITING = 'WAITING'
ACCEPTED = 'ACCEPTED'
NOT_ACCEPTED = 'NOT_ACCEPTED'
CUSTOMER_REGISTRATION_STATUS = [
    (WAITING, _('Ожидание')),
    (ACCEPTED, _('Одобрен')),
    (NOT_ACCEPTED, _('Отказано'))
]

# OPERATORS
WEB = 'WEB'
TELEGRAM = 'TELEGRAM'
WEB_OR_TELEGRAM_CHOICE = [
    (WEB, _('Web')),
    (TELEGRAM, _('Telegram'))
]
TASHKENT = 'TASHKENT'
CHINA = 'CHINA'
WAREHOUSE_CHOICE = [
    (TASHKENT, _('Tashkent')),
    (CHINA, _('China'))
]

# Loads & Products
PRODUCT_ON_WAY = 'ON_WAY'
PRODUCT_ON_WAY_DISPLAY = _('В пути')
PRODUCT_ON_WAY_DISPLAY_CUSTOMER = _('Получено в Китае')
PRODUCT_DELIVERED = 'DELIVERED'
PRODUCT_DELIVERED_DISPLAY = _('Доставлено')
PRODUCT_DELIVERED_DISPLAY_CUSTOMER = _('Получено в Ташкенте')
PRODUCT_LOADED = 'LOADED'
PRODUCT_LOADED_DISPLAY = _('Загружено')
PRODUCT_LOADED_DISPLAY_CUSTOMER = _('Ожидает выдачи')
PRODUCT_NOT_LOADED = 'NOT_LOADED'
PRODUCT_NOT_LOADED_DISPLAY = _('Не загружено')
PRODUCT_DONE = 'DONE'
PRODUCT_DONE_DISPLAY = _('Готово')
PRODUCT_DONE_DISPLAY_CUSTOMER = _('Выдано')
PRODUCT_STATUS_CHOICE = [
    (PRODUCT_ON_WAY, PRODUCT_ON_WAY_DISPLAY),
    (PRODUCT_DELIVERED, PRODUCT_DELIVERED_DISPLAY),
    (PRODUCT_LOADED, PRODUCT_LOADED_DISPLAY),
    (PRODUCT_DONE, PRODUCT_DONE_DISPLAY),
]

LOAD_NOT_PAID = 'NOT_PAID'
LOAD_PARTIALLY_PAID = 'PARTIALLY_PAID'
LOAD_PAID = 'PAID'
LOAD_CUSTOMER_DELIVERY = 'CUSTOMER_DELIVERY'
LOAD_DONE = 'DONE'
LOAD_DONE_MAIL = 'DONE_MAIL'
LOAD_STATUS_CHOICE = [
    # (CREATED, _('Created')),
    (LOAD_NOT_PAID, _('Не оплачен')),
    (LOAD_PARTIALLY_PAID, _('Частично оплачено')),
    (LOAD_PAID, _('Оплачено')),
    (LOAD_CUSTOMER_DELIVERY, _('Запрос клиента на доставку/самовывоз')),
    (LOAD_DONE, _('Готово')),
    (LOAD_DONE_MAIL, _('Готово-почта')),
]

# Tools
TAKE_AWAY = 'TAKE_AWAY'
TAKE_AWAY_DISPLAY = _('Take away')
YANDEX = 'YANDEX'
YANDEX_DISPLAY = _('Yandex')
DELIVERY_TYPE_CHOICE = [
    (TAKE_AWAY, TAKE_AWAY_DISPLAY),
    (YANDEX, YANDEX_DISPLAY),
]

NEWSLETTER_SENT = 'SENT'
NEWSLETTER_PENDING = 'PENDING'
NEWSLETTER_STATUS_CHOICE = [
    (NEWSLETTER_SENT, _('Опубликован')),
    (NEWSLETTER_PENDING, _('В ожидании'))
]

# Integrations
OFFICE_OFFICE = 1
TO_RECEIVER = 3
EMU_SERVICE_CHOICE = [
    (OFFICE_OFFICE, _('От офиса до офиса')),
    (TO_RECEIVER, _('На руки получателю')),
]
