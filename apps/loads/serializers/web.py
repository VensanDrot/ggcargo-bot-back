from datetime import datetime

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.files.models import File
from apps.loads.models import Product
from apps.tools.utils.helpers import split_code
from apps.user.models import Customer


class AdminProductListSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True, allow_null=True)
    last_update = serializers.DateTimeField(source='updated_at', read_only=True)
    responsible = serializers.SerializerMethodField(allow_null=True)

    @staticmethod
    def get_responsible(obj):
        if obj.accepted_by_china:
            responsible = obj.accepted_by_china.full_name
        else:
            responsible = obj.accepted_by_tashkent.full_name
        return responsible

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
                  'customer_id',
                  'last_update',
                  'responsible', ]


class AdminAddProductSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField(source='customer.code')
    image = serializers.SlugRelatedField(source='china_files.id', slug_field='id', queryset=File.objects.all(),
                                         required=False)

    def create(self, validated_data):
        request = self.context.get('request')

        code = validated_data.pop('customer', '')
        prefix, code = split_code(code.get('code'), request)
        image = validated_data.pop('china_files', None)
        customer = get_object_or_404(Customer, code=code, prefix=prefix)
        instance: Product = super().create(validated_data)
        instance.customer_id = customer.id
        instance.accepted_by_tashkent = request.user
        instance.accepted_time_tashkent = datetime.now()
        instance.save()
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
            prefix, code = split_code(code.get('code'), request)
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
