from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from apps.user.models import CustomerID

UserModel = get_user_model()


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            if email:
                user = user_model.objects.get(email=email)
            elif kwargs.get('code'):
                code = kwargs.get('code')
                customer_id = CustomerID.objects.get(code=code)
                user = UserModel.objects.get(email=customer_id.user.email)
                if user.check_password(password):
                    return user
            else:
                user = user_model.objects.get(email=kwargs.get('username'))
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
