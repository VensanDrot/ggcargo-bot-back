from datetime import datetime

from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404

from apps.files.models import File
from apps.loads.models import Product, Load
from apps.tools.utils.helpers import split_code, get_price
from apps.user.models import Customer
from config.core.api_exceptions import APIValidation
from config.core.choices import NOT_LOADED, NOT_LOADED_DISPLAY


class BarcodeConnectionSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField(source='customer.code')
    china_files = serializers.SlugRelatedField(slug_field='id', many=True, queryset=File.objects.all(), required=False)

    def create(self, validated_data):
        request = self.context.get('request')

        code = validated_data.pop('customer', '')
        prefix, code = split_code(code.get('code'), request)
        customer = get_object_or_404(Customer, code=code, prefix=prefix)
        instance: Product = super().create(validated_data)
        instance.customer_id = customer.id
        instance.accepted_by_china = request.user
        instance.accepted_time_china = datetime.now()
        instance.save()
        return instance

    class Meta:
        model = Product
        fields = ['barcode',
                  'customer_id',
                  'china_files', ]


class ProductListSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    @staticmethod
    def get_status(obj):
        if obj.status == 'DELIVERED':
            return NOT_LOADED
        return obj.status

    @staticmethod
    def get_status_display(obj):
        if obj.status == 'DELIVERED':
            return NOT_LOADED_DISPLAY
        return obj.get_status_display()

    @staticmethod
    def get_customer_id(obj):
        prefix = obj.customer.prefix
        code = obj.customer.code
        return f'{prefix}{code}'

    class Meta:
        model = Product
        fields = ['id',
                  'status',
                  'status_display',
                  'barcode',
                  'customer_id', ]


class AddLoadSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField()
    products = serializers.SlugRelatedField(slug_field='id', many=True, required=True, queryset=Product.objects.all())
    image = serializers.SlugRelatedField(slug_field='id', queryset=File.objects.all(), required=False)

    def load_cost(self, customer):
        weight = self.validated_data.get('weight')

        price = get_price().get('auto') if customer.user_type == 'AUTO' else get_price().get('avia')
        if price and price.isdigit():
            return float(price) * weight
        raise APIValidation('Configure price in settings', status_code=status.HTTP_400_BAD_REQUEST)

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        image = validated_data.pop('image')
        prefix, code = split_code(customer_id)
        customer = get_object_or_404(Customer, prefix=prefix, code=code)
        l_cost = self.load_cost(customer)
        instance = super().create(validated_data)
        instance.customer_id = customer.id
        instance.accepted_by = self.context.get('request').user
        instance.accepted_time = datetime.now()
        instance.save()
        image.loads_id = instance.id
        image.save()
        customer.debt += l_cost
        customer.save()
        return instance

    class Meta:
        model = Load
        fields = ['id',
                  'customer_id',
                  'weight',
                  'products',
                  'image', ]


class LoadCostDebtSerializer(serializers.Serializer):
    customer_id = serializers.CharField()
    weight = serializers.FloatField()

    def response(self, price_obj):
        data = self.validated_data
        prefix, code = split_code(data.get('customer_id'))
        customer = get_object_or_404(Customer, prefix=prefix, code=code)

        price = price_obj.get('auto') if data.get('customer_type') == 'AUTO' else price_obj.get('avia')
        if price and price.isdigit():
            return {
                'load_cost': float(price) * data.get('weight'),
                'debt': customer.debt
            }
        raise APIValidation('Configure price in settings', status_code=status.HTTP_400_BAD_REQUEST)
