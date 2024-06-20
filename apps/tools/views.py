import json
from os.path import join as join_path

from django.conf import settings
from django.db.models import Q, Count
from django.db.models.functions import TruncDate
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tools.models import Newsletter
from apps.tools.serializer import SettingsSerializer, NewsletterListSerializer, NewsletterSerializer
from apps.user.models import Customer
from config.core.api_exceptions import APIValidation
from config.core.pagination import APIPagination

settings_path = join_path(settings.BASE_DIR, 'apps', 'tools', 'settings.json')


class GetSettingsAPIView(APIView):
    serializer_class = SettingsSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: SettingsSerializer})
    def get(self, request, *args, **kwargs):
        with open(settings_path, 'r') as file:
            settings_data = json.load(file)
            serializer = self.serializer_class(data=settings_data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data)


class PostSettingsAPIView(APIView):
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
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterListSerializer
    pagination_class = APIPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['text_uz', 'text_ru', ]


class NewsletterCreateAPIView(CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class NewsletterUpdateAPIView(UpdateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    http_method_names = ['patch', ]


class NewsletterRetrieveAPIView(RetrieveAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class DashboardRegistrationAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[
        Parameter('user_type', IN_QUERY, description="Type of User: AVIA or AUTO", type=TYPE_STRING),
        Parameter('from', IN_QUERY, description="From, Date format: 2024-01-25", type=TYPE_STRING),
        Parameter('to', IN_QUERY, description="To, Date format: 2024-01-25", type=TYPE_STRING),
    ])
    def get(self, request, *args, **kwargs):
        user_type = request.query_params.get('user_type')
        # from_date = request.query_params.get('from')
        # to_date = request.query_params.get('to')
        # if user_type and from_date and to_date:
        if user_type:
            customers = Customer.objects.filter(
                Q(user_type=user_type)
                # | Q(
                #     Q(created_at__gte=from_date) | Q(created_at__lte=to_date)
                # )
            )
            # for i in customers.values_list('created_at__date', flat=True).distinct('created_at__date'):
            #     pass
            customers_per_day = Customer.objects.annotate(x=TruncDate('created_at')).values('date').annotate(
                y=Count('id')).order_by('date')

        else:
            raise APIValidation('Some of query params was missed', status_code=status.HTTP_400_BAD_REQUEST)
        return Response({'data': customers_per_day})
