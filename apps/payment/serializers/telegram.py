import xmltodict
from django.utils import timezone
from django.utils.timezone import localdate
from rest_framework import serializers, status
from django.utils.translation import gettext_lazy as _

from apps.bot.templates.text import delivery_text, request_location, mail_success
from apps.bot.utils.keyboards import location_keyboard
from apps.bot.views import avia_customer_bot, auto_customer_bot
from apps.files.models import File
from apps.integrations.emu.data import emu_order, emu_tracking_link
from apps.integrations.serializer import OrderEMUSerializer
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
            raise APIValidation(_('Эта загрузка уже оплачено'), status_code=status.HTTP_400_BAD_REQUEST)
        return obj

    def create(self, validated_data):
        user = self.context['request'].user
        if Payment.objects.filter(status__isnull=True, customer_id=user.customer.id,
                                  load=validated_data.get('load')).exists():
            raise APIValidation('Payment application with status not processed exists',
                                status_code=status.HTTP_400_BAD_REQUEST)
        try:
            customer = self.context.get('request').user.customer
            customer_id = customer.id
            image = validated_data.pop('files')
            load = validated_data.pop('load')
            payment_card = validated_data.pop('payment_card', '').replace(' ', '')
            instance = Payment.objects.create(customer_id=customer_id, load=load, payment_card=payment_card,
                                              residue=customer.debt)
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
            raise APIValidation(_('Эта загрузка не оплачено'), status_code=status.HTTP_400_BAD_REQUEST)
        delivery = load.deliveries.filter(message_sent=True)
        if delivery.exists():
            raise APIValidation(_('Вы уже получили информацию о доставке этой загрузки.'),
                                status_code=status.HTTP_400_BAD_REQUEST)
        instance: Delivery = super().create(validated_data)
        instance.customer = customer
        instance.load = load
        instance.save()

        if instance.delivery_type == 'YANDEX':
            if customer.user_type == 'AVIA':
                avia_customer_bot.send_message(chat_id=customer.tg_id, text=request_location,
                                               reply_markup=location_keyboard())
            elif customer.user_type == 'AUTO':
                auto_customer_bot.send_message(chat_id=customer.tg_id, text=request_location,
                                               reply_markup=location_keyboard())
        elif instance.delivery_type == 'MAIL':
            load.status = 'DONE_MAIL'
            data = {
                'address': instance.address,
                'customer': customer.id,
                'load': load.id,
                'phone_number': instance.phone_number,
                'service': instance.service_type,
                'town': instance.town.code
            }
            order_serializer = OrderEMUSerializer(data=data)
            order_serializer.is_valid(raise_exception=True)
            order_instance = order_serializer.save()
            order_response = emu_order(customer_full_name=request.user.full_name, order_instance=order_instance)
            order_dict = xmltodict.parse(order_response.text)
            order_instance.order_number = order_dict.get('neworder', {}).get('createorder', {}).get('@orderno')

            track_link = emu_tracking_link(order_dict.get('neworder', {}).get('createorder', {}).get('@orderno'))
            instance.track_link = track_link
            mail_message = delivery_text.format(date=localdate(timezone.now()).strftime("%d.%m.%Y"), weight=load.weight,
                                                delivery_type=instance.get_delivery_type_display(),
                                                comment=instance.comment, phone_number=customer.phone_number,
                                                track_link=track_link, customer_id=f'{customer.prefix}{customer.code}')
            mail_success_message = mail_success.format(track_link=track_link)
            if customer.user_type == 'AVIA':
                avia_customer_bot.send_message(chat_id=-1002187675934, text=mail_message, parse_mode='HTML')
                avia_customer_bot.send_message(chat_id=customer.tg_id, text=mail_success_message)
            elif customer.user_type == 'AUTO':
                auto_customer_bot.send_message(chat_id=-1002187675934, text=mail_message, parse_mode='HTML')
                auto_customer_bot.send_message(chat_id=customer.tg_id, text=mail_success_message)

            products = load.products.all()
            for product in products:
                product.status = 'DONE'
                product.save()
            load.is_active = False
            load.save()
            instance.save()
        return instance

    class Meta:
        model = Delivery
        fields = ['id',
                  'delivery_type',
                  'phone_number',
                  'town',
                  'address',
                  'service_type',
                  'comment', ]
