from django.utils import timezone
from django.utils.timezone import localdate
from rest_framework import serializers, status
from django.utils.translation import gettext_lazy as _

from apps.bot.templates.text import delivery_text, request_location
from apps.bot.utils.keyboards import location_keyboard
from apps.bot.views import avia_customer_bot, auto_customer_bot
from apps.files.models import File
from apps.payment.models import Payment
from apps.tools.models import Delivery
from config.core.api_exceptions import APIValidation


class CustomerLoadPaymentSerializer(serializers.ModelSerializer):
    image = serializers.SlugRelatedField(source='files', slug_field='id', required=True, write_only=True,
                                         queryset=File.objects.all())
    payment_card = serializers.CharField(required=True)

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
            payment_card = validated_data.pop('payment_card', '').replace(' ', '')
            instance = Payment.objects.create(customer_id=customer_id, load=load, payment_card=payment_card)
            instance.files.add(image)
            return instance
        except Exception as exc:
            raise APIValidation(f'Error occurred: {exc.args}', status_code=status.HTTP_400_BAD_REQUEST)

    class Meta:
        model = Payment
        fields = ['id',
                  'payment_card',
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
        message = delivery_text.format(date=localdate(timezone.now()).strftime("%d.%m.%Y"), weight=load.weight,
                                       delivery_type=instance.get_delivery_type_display(), comment=instance.comment,
                                       phone_number=customer.phone_number,
                                       customer_id=f'{customer.prefix}{customer.code}')
        if instance.delivery_type != 'TAKE_AWAY':
            if customer.user_type == 'AVIA':
                avia_customer_bot.send_message(chat_id=-1002187675934, text=message, parse_mode='HTML')
                if instance.delivery_type == 'YANDEX':
                    avia_customer_bot.send_message(chat_id=customer.tg_id, text=request_location,
                                                   reply_markup=location_keyboard())
            elif customer.user_type == 'AUTO':
                auto_customer_bot.send_message(chat_id=-1002187675934, text=message, parse_mode='HTML')
                if instance.delivery_type == 'YANDEX':
                    auto_customer_bot.send_message(chat_id=customer.tg_id, text=request_location,
                                                   reply_markup=location_keyboard())
        return instance

    class Meta:
        model = Delivery
        fields = ['id',
                  'delivery_type',
                  'phone_number',
                  'address',
                  'comment', ]
