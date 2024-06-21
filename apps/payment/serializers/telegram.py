from rest_framework import serializers, status
from django.utils.translation import gettext_lazy as _

from apps.files.models import File
from apps.payment.models import Payment
from apps.tools.models import Delivery
from config.core.api_exceptions import APIValidation


class CustomerLoadPaymentSerializer(serializers.ModelSerializer):
    image = serializers.SlugRelatedField(source='files', slug_field='id', required=True, write_only=True,
                                         queryset=File.objects.all())

    @staticmethod
    def validate_load(obj):
        if obj.status == 'PAID':
            raise APIValidation(_('Это загрузка уже оплачено'), status_code=status.HTTP_400_BAD_REQUEST)
        return obj

    def create(self, validated_data):
        user = self.context['request'].user
        if Payment.objects.filter(status__isnull=True, customer_id=user.customer.id,
                                  load=validated_data.get('load')).exists():
            raise APIValidation('Payment application with status not processed exists',
                                status_code=status.HTTP_400_BAD_REQUEST)
        try:
            customer_id = self.context.get('request').user.customer.id
            image = validated_data.pop('files')
            load = validated_data.pop('load')
            instance = Payment.objects.create(customer_id=customer_id, load=load)
            instance.files.add(image)
            return instance
        except Exception as exc:
            raise APIValidation(f'Error occurred: {exc.args}', status_code=status.HTTP_400_BAD_REQUEST)

    class Meta:
        model = Payment
        fields = ['id',
                  'image',
                  'load', ]


class CustomerDeliverySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context['request']
        customer = request.user.customer
        load = customer.loads.filter(is_active=True)
        if not load.exists():
            raise APIValidation(_('Загрузка не найдено'), status_code=status.HTTP_400_BAD_REQUEST)
        load = load.first()
        if load.status != 'PAID':
            raise APIValidation(_('Это загрузка не оплачено'), status_code=status.HTTP_400_BAD_REQUEST)
        if hasattr(load, 'delivery'):
            raise APIValidation(_('По этой загрузке у вас уже отправили информации доставки'),
                                status_code=status.HTTP_400_BAD_REQUEST)
        instance = super().create(validated_data)
        instance.customer = customer
        instance.load = load
        load.status = 'CUSTOMER_DELIVERY'
        load.save()
        instance.save()
        return instance

    class Meta:
        model = Delivery
        fields = ['id',
                  'delivery_type',
                  'phone_number',
                  'address',
                  'comment', ]
