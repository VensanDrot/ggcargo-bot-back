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
