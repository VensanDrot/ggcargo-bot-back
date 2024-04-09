from os import remove as delete_file

from django.utils.translation import gettext_lazy as _
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.files.models import File
from apps.files.utils import upload_file
from config.core.api_exceptions import APIValidation


class FileCreateAPIView(APIView):
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(
        operation_description="Upload file",
        manual_parameters=[
            openapi.Parameter(
                'file', in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description=_('The file to upload (max size 50 MB)')
            ),
        ]
    )
    def post(self, request):
        file = request.data.get('file')
        if not file:
            raise APIValidation(detail=_('File was not sent'), code=status.HTTP_400_BAD_REQUEST)
        if file.size > 52_428_800:
            raise APIValidation(detail=_('The file size has exceeded 50 mb!'), code=status.HTTP_400_BAD_REQUEST)

        e_file = upload_file(file=file)
        return Response({
            "message": "File successfully uploaded",
            "file": e_file.id,
            "status": status.HTTP_201_CREATED
        }, status=status.HTTP_201_CREATED)


class FileDeleteAPIView(APIView):

    @staticmethod
    def get_object(pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        file = self.get_object(pk)
        delete_file(file.path)
        file.delete()
        return Response({
            "message": "File successfully deleted",
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
