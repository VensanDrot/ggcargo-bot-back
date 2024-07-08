import json
from collections import defaultdict
from datetime import datetime
from os.path import join as join_path

from django.conf import settings
from django.utils.timezone import localdate
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
from apps.tools.serializer import SettingsSerializer, NewsletterListSerializer, NewsletterSerializer, \
    NewsletterPostSerializer
from apps.tools.tasks import send_newsletter
from apps.tools.utils.helpers import dashboard_chart_maker
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
            serializer = self.serializer_class(data=request.data, context={'settings_data': existing_settings})
            serializer.is_valid(raise_exception=True)
        with open(settings_path, 'w') as new_file:
            new_settings = dict(serializer.data)
            if new_settings:
                existing_settings.update(new_settings)
            json.dump(existing_settings, new_file, indent=2)
        existing_settings['payment_card'].pop('avia_selector')
        existing_settings['payment_card'].pop('auto_selector')
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
    serializer_class = NewsletterPostSerializer


class NewsletterUpdateAPIView(UpdateAPIView):
    permission_classes = [IsWebOperator, ]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterPostSerializer
    http_method_names = ['patch', ]


class NewsletterRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsWebOperator, ]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class FirstDashboardAPIView(APIView):
    permission_classes = [IsWebOperator, ]

    @swagger_auto_schema(manual_parameters=[
        Parameter('user_type', IN_QUERY, description="Type of User: AVIA or AUTO", type=TYPE_STRING, required=True),
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING, required=True),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING, required=True),
    ])
    # @method_decorator(cache_page(60 * 60 * 1))  # cache for an hour
    # @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        user_type = request.query_params.get('user_type')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        if user_type and from_date and to_date:
            start_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            comparing_start_date = start_date - (end_date - start_date)
            comparing_end_date = end_date - (end_date - start_date)
            loads = (Load.objects
                     .select_related('customer', 'accepted_by')
                     .prefetch_related('products')
                     .filter(created_at__date__gte=from_date, created_at__date__lte=to_date,
                             customer__user_type=user_type))
            comparing_loads = (Load.objects
                               .select_related('customer', 'accepted_by')
                               .prefetch_related('products')
                               .filter(created_at__date__gte=comparing_start_date,
                                       created_at__date__lte=comparing_end_date,
                                       customer__user_type=user_type))

            chart, totals = dashboard_chart_maker(loads, comparing_loads, start_date, end_date, date_weight_exists=True)
        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response({'chart': chart, 'totals': totals})


class SecondDashboardAPIView(APIView):
    permission_classes = [IsWebOperator, ]

    @swagger_auto_schema(manual_parameters=[
        Parameter('user_type', IN_QUERY, description="Type of User: AVIA or AUTO", type=TYPE_STRING, required=True),
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING, required=True),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING, required=True),
    ])
    # @method_decorator(cache_page(60 * 60 * 1))  # cache for an hour
    # @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        user_type = request.query_params.get('user_type')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        if user_type and from_date and to_date:
            start_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            comparing_start_date = start_date - (end_date - start_date)
            comparing_end_date = end_date - (end_date - start_date)
            loads = (Load.objects
                     .select_related('customer', 'accepted_by')
                     .prefetch_related('products')
                     .filter(created_at__date__gte=from_date, created_at__date__lte=to_date,
                             customer__user_type=user_type, status__in=['DONE', 'DONE_MAIL']))
            comparing_loads = (Load.objects
                               .select_related('customer', 'accepted_by')
                               .prefetch_related('products')
                               .filter(created_at__date__gte=comparing_start_date,
                                       created_at__date__lte=comparing_end_date,
                                       customer__user_type=user_type, status__in=['DONE', 'DONE_MAIL']))

            chart, totals = dashboard_chart_maker(loads, comparing_loads, start_date, end_date, date_weight_exists=True)
        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response({'chart': chart, 'totals': totals})


class ThirdDashboardAPIView(APIView):
    permission_classes = [IsWebOperator, ]

    @swagger_auto_schema(manual_parameters=[
        Parameter('payment_type', IN_QUERY, description="Type of Payment: CASH or CARD", type=TYPE_STRING,
                  required=True),
        Parameter('user_type', IN_QUERY, description="Type of User: AVIA or AUTO", type=TYPE_STRING, required=True),
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING, required=True),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING, required=True),
    ])
    # @method_decorator(cache_page(60 * 60 * 1))  # cache for an hour
    # @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        user_type = request.query_params.get('user_type')
        payment_type = request.query_params.get('payment_type')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        if user_type and from_date and to_date and payment_type:
            start_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            comparing_start_date = start_date - (end_date - start_date)
            comparing_end_date = end_date - (end_date - start_date)
            payments = (Payment.objects
                        .select_related('customer', 'operator', 'load')
                        .filter(created_at__date__gte=from_date, created_at__date__lte=to_date,
                                customer__user_type=user_type, payment_type=payment_type))
            comparing_payments = (Payment.objects
                                  .select_related('customer', 'operator', 'load')
                                  .filter(created_at__date__gte=comparing_start_date,
                                          created_at__date__lte=comparing_end_date,
                                          customer__user_type=user_type, payment_type=payment_type))

            chart, totals = dashboard_chart_maker(payments, comparing_payments, start_date, end_date,
                                                  date_weight_exists=False, date_payment_exists=True)
        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response({'chart': chart, 'totals': totals})


class FourthDashboardAPIView(APIView):
    permission_classes = [IsWebOperator, ]

    @swagger_auto_schema(manual_parameters=[
        Parameter('user_type', IN_QUERY, description="Type of User: AVIA or AUTO", type=TYPE_STRING, required=True),
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING, required=True),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING, required=True),
    ])
    # @method_decorator(cache_page(60 * 60 * 1))  # cache for an hour
    # @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        user_type = request.query_params.get('user_type')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        if user_type and from_date and to_date:
            start_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            comparing_start_date = start_date - (end_date - start_date)
            comparing_end_date = end_date - (end_date - start_date)
            customers = (Customer.objects
                         .select_related('passport_photo', 'accepted_by', 'user')
                         .filter(created_at__date__gte=from_date, created_at__date__lte=to_date, user_type=user_type))
            comparing_customers = (Customer.objects
                                   .select_related('passport_photo', 'accepted_by', 'user')
                                   .filter(created_at__date__gte=comparing_start_date,
                                           created_at__date__lte=comparing_end_date, user_type=user_type))

            chart, totals = dashboard_chart_maker(customers, comparing_customers, start_date, end_date,
                                                  date_weight_exists=False)
        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response({'chart': chart, 'totals': totals})


class FifthDashboardAPIView(APIView):
    permission_classes = [IsWebOperator, ]

    @swagger_auto_schema(manual_parameters=[
        Parameter('user_type', IN_QUERY, description="Type of User: AVIA or AUTO", type=TYPE_STRING, required=True),
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING, required=True),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING, required=True),
    ])
    # @method_decorator(cache_page(60 * 60 * 1))  # cache for an hour
    # @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        user_type = request.query_params.get('user_type')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        if from_date and to_date and user_type:
            products = (
                Product.objects
                .select_related('customer', 'accepted_by_china', 'accepted_by_tashkent')
                .filter(customer__user_type=user_type, created_at__date__gte=from_date, created_at__date__lte=to_date)
            )
            china = (
                products
                .filter(status='ON_WAY')
                .count()
            )
            tashkent = (
                products
                .filter(status='DELIVERED')
                .count()
            )
            waiting_delivery = (
                products
                .filter(status='LOADED')
                .count()
            )
            done = (
                products
                .filter(status='DONE')
                .count()
            )
            chart = {
                'china': china,
                'tashkent': tashkent,
                'waiting_delivery': waiting_delivery,
                'done': done
            }
        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response(chart)


class NewsletterTestAPIView(APIView):
    def get(self, request):
        send_newsletter(newsletter_id=1)
        return Response('OK')
