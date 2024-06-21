import json
from collections import defaultdict
from os.path import join as join_path

from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.timezone import localdate
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.loads.models import Load, Product
from apps.payment.models import Payment
from apps.tools.models import Newsletter
from apps.tools.serializer import SettingsSerializer, NewsletterListSerializer, NewsletterSerializer
from apps.user.models import Customer
from config.core.api_exceptions import APIValidation
from config.core.pagination import APIPagination
from config.core.permissions.web import IsWebOperator

settings_path = join_path(settings.BASE_DIR, 'apps', 'tools', 'settings.json')


class GetSettingsAPIView(APIView):
    permission_classes = [IsWebOperator, ]
    serializer_class = SettingsSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: SettingsSerializer})
    def get(self, request, *args, **kwargs):
        with open(settings_path, 'r') as file:
            settings_data = json.load(file)
            serializer = self.serializer_class(data=settings_data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data)


class PostSettingsAPIView(APIView):
    permission_classes = [IsWebOperator, ]
    serializer_class = SettingsSerializer

    @swagger_auto_schema(request_body=SettingsSerializer)
    def post(self, request, *args, **kwargs):
        with open(settings_path, 'r') as file:
            existing_settings = json.load(file)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        with open(settings_path, 'w') as new_file:
            new_settings = dict(serializer.data)
            if new_settings:
                existing_settings.update(new_settings)
            json.dump(existing_settings, new_file, indent=2)
        return Response(existing_settings)


class NewsletterListAPIView(ListAPIView):
    permission_classes = [IsWebOperator, ]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterListSerializer
    pagination_class = APIPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['text_uz', 'text_ru', ]


class NewsletterCreateAPIView(CreateAPIView):
    permission_classes = [IsWebOperator, ]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class NewsletterUpdateAPIView(UpdateAPIView):
    permission_classes = [IsWebOperator, ]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    http_method_names = ['patch', ]


class NewsletterRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsWebOperator, ]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class FirstDashboardAPIView(APIView):
    permission_classes = [IsWebOperator, ]
    @swagger_auto_schema(manual_parameters=[
        Parameter('user_type', IN_QUERY, description="Type of User: AVIA or AUTO", type=TYPE_STRING),
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING),
    ])
    # @method_decorator(cache_page(60 * 60 * 1))  # cache for an hour
    # @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        user_type = request.query_params.get('user_type')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        if user_type and from_date and to_date:
            loads = (Load.objects
                     .select_related('customer', 'accepted_by')
                     .prefetch_related('products')
                     .filter(created_at__date__gte=from_date, created_at__date__lte=to_date,
                             customer__user_type=user_type))

            date_counts = defaultdict(int)
            date_weight = defaultdict(int)
            for load in loads:
                local_date = localdate(load.created_at)
                date_counts[local_date] += 1
                date_weight[local_date] += load.weight
            sorted_dates = sorted(date_counts.keys())

            labels = [date.strftime('%Y-%m-%d') for date in sorted_dates]
            line1 = [date_counts[date] for date in sorted_dates]
            line2 = [date_weight[date] for date in sorted_dates]
            result = {
                'line1': line1,
                'line2': line2,
                'labels': labels
            }
        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response({'data': result})


class SecondDashboardAPIView(APIView):
    permission_classes = [IsWebOperator, ]
    @swagger_auto_schema(manual_parameters=[
        Parameter('user_type', IN_QUERY, description="Type of User: AVIA or AUTO", type=TYPE_STRING),
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING),
    ])
    # @method_decorator(cache_page(60 * 60 * 1))  # cache for an hour
    # @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        user_type = request.query_params.get('user_type')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        if user_type and from_date and to_date:
            loads = (Load.objects
                     .select_related('customer', 'accepted_by')
                     .prefetch_related('products')
                     .filter(created_at__date__gte=from_date, created_at__date__lte=to_date,
                             customer__user_type=user_type, status__in=['DONE', 'DONE_MAIL']))

            date_counts = defaultdict(int)
            date_weight = defaultdict(int)
            for load in loads:
                local_date = localdate(load.created_at)
                date_counts[local_date] += 1
                date_weight[local_date] += load.weight
            sorted_dates = sorted(date_counts.keys())

            labels = [date.strftime('%Y-%m-%d') for date in sorted_dates]
            line1 = [date_counts[date] for date in sorted_dates]
            line2 = [date_weight[date] for date in sorted_dates]
            result = {
                'line1': line1,
                'line2': line2,
                'labels': labels
            }
        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response({'data': result})


class ThirdDashboardAPIView(APIView):
    permission_classes = [IsWebOperator, ]
    @swagger_auto_schema(manual_parameters=[
        Parameter('user_type', IN_QUERY, description="Type of User: AVIA or AUTO", type=TYPE_STRING),
        Parameter('payment_type', IN_QUERY, description="Type of Payment: CASH or CARD", type=TYPE_STRING),
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING),
    ])
    # @method_decorator(cache_page(60 * 60 * 1))  # cache for an hour
    # @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        user_type = request.query_params.get('user_type')
        payment_type = request.query_params.get('payment_type')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        if user_type and from_date and to_date and payment_type:
            payments = (Payment.objects
                        .select_related('customer', 'operator', 'load')
                        .filter(created_at__date__gte=from_date, created_at__date__lte=to_date,
                                customer__user_type=user_type, payment_type=payment_type))

            date_counts = defaultdict(int)
            for payment in payments:
                local_date = localdate(payment.created_at)
                date_counts[local_date] += payment.paid_amount
            sorted_dates = sorted(date_counts.keys())

            labels = [date.strftime('%Y-%m-%d') for date in sorted_dates]
            line1 = [date_counts[date] for date in sorted_dates]
            result = {
                'line1': line1,
                'labels': labels
            }
        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response({'data': result})


class FourthDashboardAPIView(APIView):
    permission_classes = [IsWebOperator, ]
    @swagger_auto_schema(manual_parameters=[
        Parameter('user_type', IN_QUERY, description="Type of User: AVIA or AUTO", type=TYPE_STRING),
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING),
    ])
    # @method_decorator(cache_page(60 * 60 * 1))  # cache for an hour
    # @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        user_type = request.query_params.get('user_type')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        if user_type and from_date and to_date:
            customers = (Customer.objects
                         .select_related('passport_photo', 'accepted_by', 'user')
                         .filter(created_at__date__gte=from_date, created_at__date__lte=to_date, user_type=user_type))

            date_counts = defaultdict(int)
            for customer in customers:
                local_date = localdate(customer.created_at)
                date_counts[local_date] += 1
            sorted_dates = sorted(date_counts.keys())

            labels = [date.strftime('%Y-%m-%d') for date in sorted_dates]
            line1 = [date_counts[date] for date in sorted_dates]
            result = {
                'line1': line1,
                'labels': labels
            }
        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class FifthDashboardAPIView(APIView):
    permission_classes = [IsWebOperator, ]
    @swagger_auto_schema(manual_parameters=[
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING),
    ])
    # @method_decorator(cache_page(60 * 60 * 1))  # cache for an hour
    # @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        if from_date and to_date:
            china = (
                Product.objects
                .select_related('customer', 'accepted_by_china', 'accepted_by_tashkent')
                .filter(status='ON_WAY')
                .count()
            )
            tashkent = (
                Product.objects
                .select_related('customer', 'accepted_by_china', 'accepted_by_tashkent')
                .filter(status='DELIVERED')
                .count()
            )
            waiting_delivery = (
                Product.objects
                .select_related('customer', 'accepted_by_china', 'accepted_by_tashkent')
                .filter(status='LOADED')
                .count()
            )
            done = (
                Product.objects
                .select_related('customer', 'accepted_by_china', 'accepted_by_tashkent')
                .filter(status='DONE')
                .count()
            )
            result = {
                'china': china,
                'tashkent': tashkent,
                'waiting_delivery': waiting_delivery,
                'done': done
            }
        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response(result)
