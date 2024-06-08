from rest_framework.response import Response
from rest_framework.views import APIView

from apps.integrations.emu.data import emu_auth


class EMUAuthAPIView(APIView):
    def get(self, request, *args, **kwargs):
        response = emu_auth()
        response = response.text
        return Response(response)
