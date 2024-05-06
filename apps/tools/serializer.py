from rest_framework import serializers

from apps.tools.models import PaymentCard, Cost, ChannelLink, WarehouseAddress, SupportService


class PaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCard
        fields = ['id', 'info', 'customer_type', ]


class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost
        fields = ['id', 'info', 'customer_type', ]


class ChannelLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelLink
        fields = ['id', 'info', 'customer_type', ]


class WarehouseAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseAddress
        fields = ['id', 'info', 'customer_type', ]


class SupportServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportService
        fields = ['id', 'info', 'customer_type', ]
