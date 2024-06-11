from rest_framework import serializers

from apps.integrations.models import RegionEMU


class DistrictEMUSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionEMU
        fields = ['code',
                  'district_ru', ]
