from datetime import datetime

from django.utils.timezone import localdate, localtime
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404

from apps.files.models import File
from apps.files.serializer import FileDataSerializer
from apps.loads.models import Product, Load
from apps.tools.utils.helpers import split_code, get_price
from apps.user.models import Customer
from config.core.api_exceptions import APIValidation
from config.core.choices import TAKE_AWAY_DISPLAY, TAKE_AWAY, YANDEX, MAIL


class AdminProductListSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField(allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True, allow_null=True)
    last_update = serializers.DateTimeField(source='updated_at', read_only=True)
    responsible = serializers.SerializerMethodField(allow_null=True)
    files = FileDataSerializer(source='china_files', many=True)

    @staticmethod
    def get_responsible(obj):
        if obj.accepted_by_china:
            responsible = obj.accepted_by_china.full_name
        else:
            responsible = obj.accepted_by_tashkent.full_name
        return responsible

    @staticmethod
    def get_customer_id(obj):
        customer = obj.customer
        if customer:
            prefix = customer.prefix
            code = customer.code
            return f'{prefix}{code}'
        elif obj.is_homeless:
            return '0'
        return None

    class Meta:
        model = Product
        fields = ['id',
                  'status',
                  'status_display',
                  'barcode',
                  'customer_id',
                  'last_update',
                  'responsible',
                  'files', ]


class AdminAddProductSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField(source='customer.code')
    image = serializers.SlugRelatedField(source='china_files.id', slug_field='id', queryset=File.objects.all(),
                                         required=False, write_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['customer_id'] = f'{instance.customer.prefix}{instance.customer.code}'
        # representation['status'] = instance.status
        representation['status_display'] = instance.get_status_display()
        representation['last_update'] = localtime(instance.updated_at)
        responsible_user = instance.accepted_by_china or instance.accepted_by_tashkent
        representation['responsible'] = responsible_user.full_name or responsible_user.full_name
        representation['files'] = FileDataSerializer(instance.china_files.all(), many=True).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        code = validated_data.pop('customer', '')
        prefix, code = split_code(code.get('code'))
        image = validated_data.pop('china_files', None)
        customer = get_object_or_404(Customer, code=code, prefix=prefix)
        instance: Product = super().create(validated_data)
        instance.customer_id = customer.id
        instance.accepted_by_tashkent = request.user
        instance.accepted_time_tashkent = datetime.now()
        instance.save()
        if image:
            file = image.get('id')
            file.china_product_id = instance.id
            file.save()
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')

        code = validated_data.pop('customer', '')
        image = validated_data.pop('china_files', {})
        instance = super().update(instance, validated_data)
        if code:
            prefix, code = split_code(code.get('code'))
            customer = get_object_or_404(Customer, code=code, prefix=prefix)
            instance.customer_id = customer.id
        instance.accepted_by_tashkent = request.user
        instance.accepted_time_tashkent = datetime.now()
        instance.save()
        if image.get('id'):
            file = image.get('id')
            file.china_product_id = instance.id
            file.save()
        return instance

    class Meta:
        model = Product
        fields = ['id',
                  'barcode',
                  'customer_id',
                  'image',
                  'status', ]


class AdminLoadListSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField(allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True, allow_null=True)
    customer_id = serializers.SerializerMethodField(allow_null=True)
    files = FileDataSerializer(many=True, allow_null=True)

    @staticmethod
    def get_customer_id(obj):
        customer = obj.customer
        if customer:
            return f'{customer.prefix}{customer.code}'
        return None

    @staticmethod
    def get_updated_at(obj):
        if obj.updated_at:
            return localdate(obj.updated_at)
        return None

    class Meta:
        model = Load
        fields = ['id',
                  'customer_id',
                  'weight',
                  'cost',
                  'status',
                  'status_display',
                  'updated_at',
                  'files', ]


class ProductListSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField(allow_null=True)

    @staticmethod
    def get_updated_at(obj):
        if obj.updated_at:
            return localdate(obj.updated_at)
        return None

    class Meta:
        model = Product
        fields = ['barcode',
                  'updated_at']


class AdminLoadRetrieveSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField(allow_null=True)
    status_display = serializers.CharField(source='get_status_display', allow_null=True)
    debt = serializers.CharField(source='customer.debt', allow_null=True)
    products = ProductListSerializer(many=True, allow_null=True)
    files = FileDataSerializer(many=True, allow_null=True)
    address = serializers.SerializerMethodField(allow_null=True)

    @staticmethod
    def get_address(obj):
        if hasattr(obj, 'delivery'):
            delivery = obj.delivery
            if delivery.delivery_type == TAKE_AWAY:
                return TAKE_AWAY_DISPLAY
            elif delivery.delivery_type == YANDEX:
                return delivery.address
            elif delivery.delivery_type == MAIL:
                return delivery.address
        return _('Нет информации о доставки')

    @staticmethod
    def get_customer_id(obj):
        customer = obj.customer
        if customer:
            return f'{customer.prefix}{customer.code}'
        return None

    class Meta:
        model = Load
        fields = ['id',
                  'customer_id',
                  'weight',
                  'cost',
                  'status',
                  'status_display',
                  'debt',
                  'products',
                  'files',
                  'address', ]


class AdminLoadUpdateSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField(required=True)

    def load_cost(self, customer):
        weight = self.validated_data.get('weight')
        price = get_price().get('auto') if customer.user_type == 'AUTO' else get_price().get('avia')
        if price:
            return float(price) * weight
        raise APIValidation('Configure price in settings', status_code=status.HTTP_400_BAD_REQUEST)

    def update(self, instance, validated_data):
        customer_id = validated_data.pop('customer_id', '')
        if not customer_id:
            raise APIValidation(_('customer_id - обязательное поле'), status_code=status.HTTP_400_BAD_REQUEST)

        prefix, code = split_code(customer_id)
        customer = get_object_or_404(Customer, prefix=prefix, code=code)
        if validated_data.get('weight'):
            new_cost = self.load_cost(customer)
            old_cost = instance.cost
            debt = customer.debt
            cost_diff = old_cost - new_cost
            debt += cost_diff
            customer.debt = debt
            customer.save()
            instance.cost = new_cost
        if customer_id:
            instance.customer = customer
        instance.save()
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance: Load):
        representation = super().to_representation(instance)
        representation['status_display'] = instance.get_status_display()
        representation['updated_at'] = localdate(instance.updated_at)
        representation['cost'] = instance.cost
        representation['customer_id'] = f"{instance.customer.prefix}{instance.customer.code}"
        representation['files'] = FileDataSerializer(instance.files.all(), many=True).data
        return representation

    class Meta:
        model = Load
        fields = ['id',
                  'customer_id',
                  'status',
                  'weight', ]
