from rest_framework import serializers

from apps.integrations.models import RegionEMU, OrderEMU


class DistrictEMUSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionEMU
        fields = ['code',
                  'district_ru', ]


class OrderEMUSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEMU
        fields = ['phone_number',
                  'address',
                  'town',
                  'service',
                  'customer',
                  'load', ]
