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
PREFIX_CHOICES = [
    (WSC, 'WSC'),
    (YDQ, 'YDQ'),
    (ZRD, 'ZRD'),
    (HVP, 'HVP'),
    (LXE, 'LXE'),
    (GZG, 'GZG'),
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
ON_WAY = 'ON_WAY'
ON_WAY_DISPLAY = _('В пути')
ON_WAY_DISPLAY_CUSTOMER = _('Получено в Китае')
DELIVERED = 'DELIVERED'
DELIVERED_DISPLAY = _('Доставлено')
DELIVERED_DISPLAY_CUSTOMER = _('Получено в Ташкенте')
LOADED = 'LOADED'
LOADED_DISPLAY = _('Загружено')
LOADED_DISPLAY_CUSTOMER = _('Ожидает выдачи')
NOT_LOADED = 'NOT_LOADED'
NOT_LOADED_DISPLAY = _('Не загружено')
DONE = 'DONE'
DONE_DISPLAY = _('Готово')
DONE_DISPLAY_CUSTOMER = _('Выдано')
PRODUCT_STATUS_CHOICE = [
    (ON_WAY, ON_WAY_DISPLAY),
    (DELIVERED, DELIVERED_DISPLAY),
    (LOADED, LOADED_DISPLAY),
    (DONE, DONE_DISPLAY),
]

NOT_PAID = 'NOT_PAID'
PARTIALLY_PAID = 'PARTIALLY_PAID'
PAID = 'PAID'
DONE = 'DONE'
CUSTOMER_DELIVERY = 'CUSTOMER_DELIVERY'
DONE_MAIL = 'DONE_MAIL'
STATUS_CHOICE = [
    # (CREATED, _('Created')),
    (NOT_PAID, _('Не оплачен')),
    (PARTIALLY_PAID, _('Частично оплачено')),
    (PAID, _('Оплачено')),
    (CUSTOMER_DELIVERY, _('Запрос клиента на доставку/самовывоз')),
    (DONE, _('Готово')),
    (DONE_MAIL, _('Готово-почта')),
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
