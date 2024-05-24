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

NONE = None
ACCEPTED = 'ACCEPTED'
NOT_ACCEPTED = 'NOT_ACCEPTED'
CUSTOMER_REGISTRATION_STATUS = [
    (None, _('Waiting')),
    (ACCEPTED, _('Accepted')),
    (NOT_ACCEPTED, _('Not accepted'))
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

# PRODUCTS
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
