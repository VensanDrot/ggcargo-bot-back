from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.files.models import File
from apps.loads.models import Product
from apps.user.models import CustomerID


class BarcodeConnectionSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField(source='customer_code.code')
    china_files = serializers.SlugRelatedField(slug_field='id', many=True, queryset=File.objects.all())

    def create(self, validated_data):
        code = validated_data.pop('customer_code', '')
        code_obj = get_object_or_404(CustomerID, code=code.get('code'))
        instance: Product = super().create(validated_data)
        instance.customer_code_id = code_obj.id
        instance.save()
        return instance

    class Meta:
        model = Product
        fields = ['barcode',
                  'customer_id',
                  'china_files', ]


class AcceptProductSerializer(serializers.ModelSerializer):
    tashkent_files = serializers.SlugRelatedField(slug_field='id', many=True, queryset=File.objects.all())

    class Meta:
        model = Product
        fields = ['tashkent_files']
