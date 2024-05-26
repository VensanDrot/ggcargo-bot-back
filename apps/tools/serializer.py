from rest_framework import serializers

from apps.files.serializer import FileDataSerializer
from apps.tools.models import Newsletter
from config.core.api_exceptions import APIValidation


class SettingToolSerializer(serializers.Serializer):
    avia = serializers.CharField(allow_null=True, required=False)
    auto = serializers.CharField(allow_null=True, required=False)


class PriceToolSerializer(serializers.Serializer):
    avia = serializers.IntegerField(allow_null=True, required=False)
    auto = serializers.IntegerField(allow_null=True, required=False)


class PaymentCardToolSerializer(serializers.Serializer):
    avia = serializers.CharField(allow_null=True, required=False)
    auto = serializers.CharField(allow_null=True, required=False)

    @staticmethod
    def get_avia(value):
        if value:
            if value.isdigit():
                p_card = value.replace(' ', '')
            else:
                raise APIValidation('Payment card includes only digits (payment-card 16 digits)')
            if len(p_card) != 16:
                raise APIValidation('Payment card should have 16 digits')
            return p_card
        return value

    @staticmethod
    def get_auto(value):
        if value:
            if value.isdigit():
                p_card = value.replace(' ', '')
            else:
                raise APIValidation('Payment card includes only digits (payment-card 16 digits)')
            if len(p_card) != 16:
                raise APIValidation('Payment card should have 16 digits')
            return p_card
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['avia'] = self.get_avia(representation['avia'])
        representation['auto'] = self.get_auto(representation['auto'])
        return representation


class SettingsSerializer(serializers.Serializer):
    payment_card = PaymentCardToolSerializer(required=False)
    price = PriceToolSerializer(required=False)
    address = SettingToolSerializer(required=False)
    link = SettingToolSerializer(required=False)
    support = SettingToolSerializer(required=False)


class NewsletterListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    # photo_uz = FileDataSerializer(allow_null=True)
    # photo_ru = FileDataSerializer(allow_null=True)

    class Meta:
        model = Newsletter
        fields = ['id',
                  'send_date',
                  'bot_type',
                  'text_uz',
                  'text_ru',
                  # 'photo_uz',
                  # 'photo_ru',
                  'status',
                  'status_display', ]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id',
                  'send_date',
                  'bot_type',
                  'text_uz',
                  'text_ru',
                  'photo_uz',
                  'photo_ru', ]
