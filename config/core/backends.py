from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, is_telegram=None, **kwargs):
        user_model = get_user_model()
        try:
            if is_telegram:
                user = user_model.objects.get(operator__tg_id=username, operator__warehouse=kwargs['warehouse'])
                return user
            user = user_model.objects.get(
                Q(email=username) | Q(operator__tg_id=username) |
                (Q(customer__prefix=username[:3]) & Q(customer__code=username[3:]))
            )
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
