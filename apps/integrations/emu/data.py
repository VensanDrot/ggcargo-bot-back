import requests
from django.conf import settings

emu_integration = settings.INTEGRATIONS['EMU']


def emu_auth():
    url = 'https://home.courierexe.ru/api/'
    emu_creds = emu_integration['credentials']
    emu_extra = emu_integration['extra']
    xml = f"""
    <auth extra="{emu_extra}" login="{emu_creds['username']}" pass="{emu_creds['password']}"></auth>
    """
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(url, data=xml, headers=headers)
    return response
