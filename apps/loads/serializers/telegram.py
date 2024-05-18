from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import localdate
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404

from apps.files.models import File
from apps.files.serializer import FileDataSerializer
from apps.loads.models import Product, Load
from apps.payment.models import Payment
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
        instance.accepted_time_china = timezone.now()
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
    updated_at = serializers.SerializerMethodField(allow_null=True, read_only=True)

    @staticmethod
    def get_updated_at(obj):
        if obj.updated_at:
            return obj.updated_at.date()
        return obj.updated_at

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
                  'status_display',
                  'updated_at', ]


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
        try:
            customer_id = validated_data.pop('customer_id')
            products = validated_data.get('products')
            image = validated_data.pop('image')
            prefix, code = split_code(customer_id)
            customer = get_object_or_404(Customer, prefix=prefix, code=code)
            l_cost = self.load_cost(customer)
            existing_load = Load.objects.filter(customer_id=customer.id, status='CREATED')
            if existing_load.exists():
                existing_load = existing_load.first()
                image.loads_id = existing_load.id
                image.save()
                customer.debt += l_cost
                customer.save()
                existing_load.loads_count += 1
                existing_load.weight += validated_data.get('weight')
                existing_load.products.add(*products)
                existing_load.save()
                for product in products:
                    product.status = 'LOADED'
                    product.save()
                return existing_load
            instance = super().create(validated_data)
            instance.customer_id = customer.id
            instance.accepted_by = self.context.get('request').user
            instance.accepted_time = timezone.now()
            instance.save()
            image.loads_id = instance.id
            image.save()
            customer.debt += l_cost
            customer.save()
            for product in products:
                product.status = 'LOADED'
                product.save()
            return instance
        except Exception as exc:
            raise APIValidation(f'Error occurred {exc.args}', status_code=status.HTTP_400_BAD_REQUEST)

    class Meta:
        model = Load
        fields = ['id',
                  'customer_id',
                  'weight',
                  'products',
                  'image', ]


class ModerationNotProcessedLoadSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField(allow_null=True)
    debt = serializers.CharField(source='customer.debt', allow_null=True)
    date = serializers.SerializerMethodField(allow_null=True)

    @staticmethod
    def get_date(obj):
        return localdate(obj.created_at)

    @staticmethod
    def get_customer_id(obj):
        customer = obj.customer
        return f"{customer.prefix}{customer.code}"

    class Meta:
        model = Payment
        fields = ['id',
                  'customer_id',
                  'debt',
                  'date', ]


class ModerationProcessedLoadSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField(allow_null=True)
    debt = serializers.CharField(source='customer.debt', allow_null=True)
    date = serializers.SerializerMethodField(allow_null=True)
    status_display = serializers.CharField(source='get_status_display', allow_null=True)

    @staticmethod
    def get_date(obj):
        return localdate(obj.created_at)

    @staticmethod
    def get_customer_id(obj):
        customer = obj.customer
        return f"{customer.prefix}{customer.code}"

    class Meta:
        model = Payment
        fields = ['id',
                  'customer_id',
                  'debt',
                  'date',
                  'status',
                  'status_display', ]


class ModerationLoadPaymentSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField(allow_null=True)
    date = serializers.SerializerMethodField(allow_null=True)
    debt = serializers.CharField(source='customer.debt', allow_null=True)

    @staticmethod
    def get_date(obj):
        return localdate(obj.created_at)

    @staticmethod
    def get_customer_id(obj):
        customer = obj.customer
        return f"{customer.prefix}{customer.code}"

    class Meta:
        model = Payment
        fields = ['id',
                  'customer_id',
                  'date',
                  'debt', ]


class ModerationLoadApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id',
                  'paid_amount',
                  'comment', ]


class ModerationLoadDeclineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id',
                  'comment', ]


# CUSTOMER

class CustomerProductsSerializer(serializers.ModelSerializer):
    files = FileDataSerializer(source='china_files', many=True, allow_null=True)
    status = serializers.SerializerMethodField(read_only=True, allow_null=True)
    status_display = serializers.SerializerMethodField(read_only=True, allow_null=True)
    updated_at = serializers.SerializerMethodField(allow_null=True, read_only=True)

    @staticmethod
    def get_updated_at(obj):
        if obj.updated_at:
            return obj.updated_at.date()
        return obj.updated_at

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
                  'status_display',
                  'files',
                  'updated_at', ]


class CustomerCurrentLoadSerializer(serializers.ModelSerializer):
    products = CustomerProductsSerializer(many=True, allow_null=True)
    debt = serializers.CharField(source='customer.debt', allow_null=True)

    class Meta:
        model = Load
        fields = ['id',
                  'status',
                  'weight',
                  'debt',
                  'products', ]


class CustomerOwnLoadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Load
        fields = ['id',
                  'status',
                  'updated_at', ]
