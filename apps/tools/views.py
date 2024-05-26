import json
from os.path import join as join_path

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tools.models import Newsletter
from apps.tools.serializer import SettingsSerializer, NewsletterListSerializer, NewsletterSerializer

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
