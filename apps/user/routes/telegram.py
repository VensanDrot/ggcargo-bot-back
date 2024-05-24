from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.user.models import User
from apps.user.serializers.telegram import (CustomerAviaRegistrationStepOneSerializer,
                                            CustomerAviaRegistrationStepTwoSerializer,
                                            CustomerAviaRegistrationStepThreeSerializer,
                                            CustomerAutoRegistrationStepOneSerializer,
                                            CustomerAutoRegistrationStepTwoSerializer,
                                            CustomerSettingsPersonalRetrieveSerializer,
                                            CustomerSettingsPersonalUpdateSerializer,
                                            CustomerSettingsPasswordUpdateSerializer)
from config.core.api_exceptions import APIValidation
from config.core.permissions.telegram import IsCustomer


class CustomerAviaRegistrationStepOneAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerAviaRegistrationStepOneSerializer
    permission_classes = [AllowAny, ]


class CustomerAviaRegistrationStepTwoAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerAviaRegistrationStepTwoSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['patch', ]


class CustomerAviaRegistrationStepThreeAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerAviaRegistrationStepThreeSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['patch', ]


class CustomerAutoRegistrationStepOneAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerAutoRegistrationStepOneSerializer
    permission_classes = [AllowAny, ]


class CustomerAutoRegistrationStepTwoAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerAutoRegistrationStepTwoSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['patch', ]


class CustomerSettingsPersonalRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSettingsPersonalRetrieveSerializer
    permission_classes = [IsCustomer, ]
    lookup_field = None

    def get_object(self):
        return self.request.user


class CustomerSettingsPersonalUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSettingsPersonalUpdateSerializer
    permission_classes = [IsCustomer, ]
    http_method_names = ['patch', ]
    lookup_field = None

    def get_object(self):
        return self.request.user


class CustomerSettingsPasswordUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSettingsPasswordUpdateSerializer
    permission_classes = [IsCustomer, ]
    http_method_names = ['patch', ]
    lookup_field = None

    def get_object(self):
        return self.request.user
