from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Parameter, IN_FORM, IN_BODY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bot.templates.text import reg_moderation_accept_uz, reg_moderation_accept_ru, reg_moderation_decline_ru, \
    reg_moderation_decline_uz
from apps.bot.views import avia_customer_bot, auto_customer_bot
from apps.files.models import File
from apps.user.filter import UserStaffFilter, CustomerModerationFilter, CustomerSearchFilter, \
    CustomerModerationSearchFilter
from apps.user.models import User, Customer, CustomerRegistration
from apps.user.serializers.web import (PostUserSerializer, GetUserSerializer, PostCustomerSerializer,
                                       GetCustomerSerializer, RetrieveCustomerSerializer,
                                       PostResponseCustomerSerializer, PostResponseUserSerializer,
                                       CustomerModerationListSerializer, CustomerModerationRetrieveSerializer,
                                       CustomerModerationDeclineSerializer, CustomerModerationAcceptSerializer)
from config.core.api_exceptions import APIValidation
from config.core.pagination import APIPagination
from config.core.permissions import IsOperator
from config.views import ModelViewSetPack


class UserModelViewSet(ModelViewSetPack):
    queryset = User.objects.filter(operator__isnull=False)
    serializer_class = GetUserSerializer
    permission_classes = [IsOperator, ]
    post_serializer_class = PostUserSerializer
    pagination_class = APIPagination
    filterset_class = UserStaffFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['full_name', 'operator__tg_id', 'email']

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                response_serializer = PostResponseUserSerializer(instance=instance)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIValidation(f'Error occurred: {e.args[0]}', status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PostResponseUserSerializer)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            new_instance = self.get_object()
            response_serializer = PostResponseUserSerializer(instance=new_instance)
            response = response_serializer.data
            return Response(response)
        except Exception as e:
            raise APIValidation(f'Error occurred: {e.args[0]}', status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PostUserSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class CustomerModelViewSet(ModelViewSetPack):
    queryset = User.objects.filter(customer__isnull=False, is_active=True)
    serializer_class = GetCustomerSerializer
    permission_classes = [IsOperator, ]
    post_serializer_class = PostCustomerSerializer
    pagination_class = APIPagination
    filter_backends = [DjangoFilterBackend, CustomerSearchFilter]
    search_fields = ['customer__user_type', 'customer__prefix', 'customer__code', 'full_name', 'customer__phone_number',
                     'customer__debt']

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return RetrieveCustomerSerializer(args[0])
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                response_serializer = PostResponseCustomerSerializer(instance=instance)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIValidation(f'Error occurred: {e.args[0]}', status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PostCustomerSerializer)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            new_instance = self.get_object()
            response_serializer = PostResponseCustomerSerializer(instance=new_instance)
            response = response_serializer.data
            return Response(response)
        except Exception as e:
            raise APIValidation(f'Error occurred: {e.args[0]}', status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PostCustomerSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class CustomerIDPrefix(APIView):
    """
    url-parameter choices: AVIA and AUTO
    """
    permission_classes = [IsOperator, ]

    @staticmethod
    def get(request, *args, **kwargs):
        user_type = kwargs.get('user_type')
        if user_type == 'AUTO':
            response = [{'prefix': 'G'}, {'prefix': 'E'}, {'prefix': 'X'}, ]
        elif user_type == 'AVIA':
            response = [{'prefix': 'W'}, {'prefix': 'M'}, {'prefix': 'Z'}]
        else:
            raise APIValidation("Url parameter (user_type) accepts only AUTO or AVIA",
                                status_code=status.HTTP_400_BAD_REQUEST)
        return Response(response)


class CustomerModerationListAPIView(ListAPIView):
    queryset = CustomerRegistration.objects.select_related('customer').filter(done=True)
    serializer_class = CustomerModerationListSerializer
    permission_classes = [IsOperator, ]
    pagination_class = APIPagination
    filterset_class = CustomerModerationFilter
    filter_backends = [DjangoFilterBackend, CustomerModerationSearchFilter, ]
    search_fields = ['customer__user_type', 'customer__prefix', 'customer__code', 'customer__user__full_name',
                     'customer__phone_number', 'customer__accepted_by__full_name']


class CustomerModerationRetrieveAPIView(RetrieveAPIView):
    queryset = CustomerRegistration.objects.select_related('customer').filter(done=True)
    serializer_class = CustomerModerationRetrieveSerializer
    permission_classes = [IsOperator, ]


class CustomerModerationDeclineAPIView(APIView):
    serializer_class = CustomerModerationDeclineSerializer
    permission_classes = [IsOperator, ]

    @swagger_auto_schema(request_body=CustomerModerationDeclineSerializer)
    def post(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        customer_registration = get_object_or_404(CustomerRegistration, pk=pk)
        if customer_registration.status != 'WAITING':
            raise APIValidation(_('Эта заявка уже была обработана'), status_code=status.HTTP_400_BAD_REQUEST)
        customer_registration.reject_message = data.get('reject_message')
        customer_registration.customer.accepted_by = request.user
        customer_registration.status = 'NOT_ACCEPTED'
        customer_registration.save()
        customer_registration.customer.save()

        customer = customer_registration.customer
        customer.prefix = None
        customer.code = None
        customer.phone_number = customer.phone_number + ' '
        customer.save()

        response_serializer = CustomerModerationRetrieveSerializer(instance=customer_registration)
        response = response_serializer.data
        if customer.language == 'uz':
            message = reg_moderation_decline_uz.format(reject_message=customer_registration.reject_message)
        else:
            message = reg_moderation_decline_ru.format(reject_message=customer_registration.reject_message)
        if customer.user_type == 'AUTO':
            auto_customer_bot.send_message(chat_id=customer.tg_id, text=message)
        elif customer.user_type == 'AVIA':
            avia_customer_bot.send_message(chat_id=customer.tg_id, text=message)
        return Response(response)


class CustomerModerationAcceptAPIView(APIView):
    serializer_class = CustomerModerationAcceptSerializer
    permission_classes = [IsOperator, ]

    @swagger_auto_schema(request_body=CustomerModerationAcceptSerializer)
    def post(self, request, pk, *args, **kwargs):
        customer_registration = get_object_or_404(CustomerRegistration, pk=pk)
        if customer_registration.status != 'WAITING':
            raise APIValidation(_('Эта заявка уже была обработана'), status_code=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict = serializer.validated_data
        if data.get('passport_photo'):
            get_object_or_404(File, pk=data.get('passport_photo'))

        customer = customer_registration.customer
        user = customer.user
        customer_registration.status = 'ACCEPTED'
        user.is_active = True
        user.full_name = data.get('full_name', user.full_name)
        customer.accepted_by = request.user
        customer.phone_number = data.get('phone_number', customer.phone_number)
        customer.birth_date = data.get('birth_date', customer.birth_date)
        customer.passport_serial_number = data.get('passport_serial_number', customer.passport_serial_number)
        customer.passport_photo_id = data.get('passport_photo', customer.passport_photo_id)
        user.save()
        customer.save()
        customer_registration.save()

        response_serializer = CustomerModerationRetrieveSerializer(instance=customer_registration)
        response = response_serializer.data
        if customer.language == 'uz':
            message = reg_moderation_accept_uz.format(customer_id=f'{customer.prefix}{customer.code}')
        else:
            message = reg_moderation_accept_ru.format(customer_id=f'{customer.prefix}{customer.code}')
        if customer.user_type == 'AUTO':
            auto_customer_bot.send_message(chat_id=customer.tg_id, text=message)
        elif customer.user_type == 'AVIA':
            avia_customer_bot.send_message(chat_id=customer.tg_id, text=message)
        return Response(response)
