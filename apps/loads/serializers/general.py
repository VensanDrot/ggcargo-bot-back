from rest_framework import serializers

from apps.loads.models import Product


class OpenProductBarcodeSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')

    class Meta:
        model = Product
        fields = ['status',
                  'status_display', ]
