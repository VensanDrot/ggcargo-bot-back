from datetime import datetime

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.files.models import File
from apps.loads.models import Product
from apps.tools.utils.helpers import split_code
from apps.user.models import Customer, Operator


class OperatorStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator


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


class AcceptProductSerializer(serializers.ModelSerializer):
    tashkent_files = serializers.SlugRelatedField(slug_field='id', many=True, required=False,
                                                  queryset=File.objects.all())

    class Meta:
        model = Product
        fields = ['tashkent_files']
