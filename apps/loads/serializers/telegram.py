from datetime import datetime

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.files.models import File
from apps.loads.models import Product, Load
from apps.tools.utils.helpers import split_code
from apps.user.models import Customer


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


class AcceptProductSerializer(serializers.ModelSerializer):
    tashkent_files = serializers.SlugRelatedField(slug_field='id', many=True, required=False,
                                                  queryset=File.objects.all())

    class Meta:
        model = Product
        fields = ['tashkent_files']


class ProductListSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    # @staticmethod
    # def get_status(obj):
    #     if obj.status == 'DELIVERED':
    #         return NOT_LOADED
    #     return obj.status
    #
    # @staticmethod
    # def get_status_display(obj):
    #     if obj.status == 'DELIVERED':
    #         return NOT_LOADED_DISPLAY
    #     return obj.get_status_display()

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
    customer_id = serializers.SerializerMethodField()
    products = serializers.SlugRelatedField(slug_field='id', many=True, required=True, queryset=Product.objects.all())
    image = serializers.SlugRelatedField(source='loads.id', slug_field='id', queryset=File.objects.all(),
                                         required=False)

    @staticmethod
    def get_customer_id(obj):
        return 'Test'

    class Meta:
        model = Load
        fields = ['id',
                  'customer_id',
                  'weight',
                  'products',
                  'image', ]
