from datetime import datetime

from django.db.models import Q
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
        prefix, code = split_code(code.get('code'))
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


class ProductSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True, allow_null=True)
    status_display = serializers.SerializerMethodField(read_only=True, allow_null=True)

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

    class Meta:
        model = Product
        fields = ['id',
                  'barcode',
                  'status',
                  'status_display']


class LoadInfoSerializer(serializers.Serializer):
    customer_id = serializers.CharField(write_only=True)
    weight = serializers.FloatField()

    # @staticmethod
    # def get_customer_id(obj):
    #     prefix = obj.customer.prefix
    #     code = obj.customer.code
    #     return f'{prefix}{code}'

    def response(self, price_obj):
        data = self.validated_data
        prefix, code = split_code(data.get('customer_id'))
        customer = get_object_or_404(Customer, prefix=prefix, code=code)
        products = customer.products.filter(
            (Q(customer__prefix=prefix) & Q(customer__code=code)) & Q(status='DELIVERED')
        )
        products_serializer = ProductSerializer(products, many=True)
        price = price_obj.get('auto') if data.get('customer_type') == 'AUTO' else price_obj.get('avia')
        if not price:
            raise APIValidation('Configure price in settings', status_code=status.HTTP_400_BAD_REQUEST)
        return {
            'load_cost': float(price) * data.get('weight'),
            'debt': customer.debt,
            'products': products_serializer.data,
        }


class AddLoadSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField()
    products = serializers.SlugRelatedField(slug_field='id', many=True, required=True, queryset=Product.objects.all())
    image = serializers.SlugRelatedField(slug_field='id', queryset=File.objects.all(), required=False)

    def validate_products(self, value):
        customer_id = self.context.get('request').data.get('customer_id')
        prefix, code = split_code(customer_id)
        for product in value:
            if product.status != 'DELIVERED':
                raise APIValidation(f'Product #{product.id} was not delivered or already loaded',
                                    status_code=status.HTTP_400_BAD_REQUEST)
            if product.customer.prefix != prefix or product.customer.code != code:
                raise APIValidation(f"Customer#{customer_id} with such products not found",
                                    status_code=status.HTTP_400_BAD_REQUEST)
        return value

    def load_cost(self, customer):
        weight = self.validated_data.get('weight')

        price = get_price().get('auto') if customer.user_type == 'AUTO' else get_price().get('avia')
        if price:
            return float(price) * weight
        raise APIValidation('Configure price in settings', status_code=status.HTTP_400_BAD_REQUEST)

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        products = validated_data.get('products')
        image = validated_data.pop('image')
        prefix, code = split_code(customer_id)
        customer = get_object_or_404(Customer, prefix=prefix, code=code)
        l_cost = self.load_cost(customer)
        existing_load = Load.objects.filter(customer_id=customer.id, status='CREATED')
        if existing_load.exists():
            return existing_load
        instance = super().create(validated_data)
        instance.customer_id = customer.id
        instance.accepted_by = self.context.get('request').user
        instance.accepted_time = datetime.now()
        instance.save()
        image.loads_id = instance.id
        image.save()
        customer.debt += l_cost
        customer.save()
        for product in products:
            product.status = 'LOADED'
            product.save()
        return instance

    class Meta:
        model = Load
        fields = ['id',
                  'customer_id',
                  'weight',
                  'products',
                  'image', ]


class ModerationNotProcessedLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Load
        fields = ['id',
                  # 'customer_id',
                  ]
