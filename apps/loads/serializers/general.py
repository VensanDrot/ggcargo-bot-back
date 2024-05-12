from rest_framework import serializers, status

from config.core.api_exceptions import APIValidation
from config.core.choices import CAR_OR_AIR_CHOICE


class LoadCostSerializer(serializers.Serializer):
    customer_type = serializers.ChoiceField(choices=CAR_OR_AIR_CHOICE)
    weight = serializers.FloatField()

    def calculate_cost(self, price_obj):
        data = self.validated_data
        price = price_obj.get('auto') if data.get('customer_type') == 'AUTO' else price_obj.get('avia')
        if price and price.isdigit():
            return float(price) * data.get('weight')
        raise APIValidation('Configure price in settings', status_code=status.HTTP_400_BAD_REQUEST)
