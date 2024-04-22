from datetime import datetime

from rest_framework import status

from config.core.api_exceptions import APIValidation


def split_code(full_code, request):
    prefix = ""
    code = ""

    for char in full_code:
        if char.isdigit():
            code += char
        else:
            prefix += char
    user_company_type = request.user.company_type
    if user_company_type != prefix:
        raise APIValidation("Not allowed for this customer", status_code=status.HTTP_400_BAD_REQUEST)
    return prefix, code


def accepted_today(user):
    if user.products_china.exists():
        count = user.products_china.filter(accepted_time_china__date=datetime.now().date()).count()
    else:
        count = user.products_tashkent.filter(accepted_time_tashkent__date=datetime.now().date()).count()
    return count
