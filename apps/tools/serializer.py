from django.utils.timezone import localtime
from rest_framework import serializers

from apps.files.serializer import FileDataSerializer
from apps.tools.models import Newsletter
from apps.tools.tasks import create_newsletter_task


class SettingToolSerializer(serializers.Serializer):
    avia = serializers.CharField(allow_null=True, required=False)
    auto = serializers.CharField(allow_null=True, required=False)


class PriceToolSerializer(serializers.Serializer):
    avia = serializers.IntegerField(allow_null=True, required=False)
    auto = serializers.IntegerField(allow_null=True, required=False)


class PaymentCardToolSerializer(serializers.Serializer):
    avia = serializers.CharField(allow_null=True, required=False)
    auto = serializers.CharField(allow_null=True, required=False)

    def get_avia(self, value):
        settings_data = self.context['settings_data']
        if value:
            p_card = value.replace(' ', '')
            return p_card
        return settings_data['payment_card']['avia'], settings_data['payment_card']['avia_selector']

    def get_auto(self, value):
        settings_data = self.context['settings_data']
        if value:
            p_card = value.replace(' ', '')
            return p_card
        return settings_data['payment_card']['auto'], settings_data['payment_card']['auto_selector']

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
    photo_uz = FileDataSerializer(allow_null=True)
    photo_ru = FileDataSerializer(allow_null=True)

    class Meta:
        model = Newsletter
        fields = ['id',
                  'send_date',
                  'bot_type',
                  'text_uz',
                  'text_ru',
                  'photo_uz',
                  'photo_ru', ]


class NewsletterPostSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['photo_uz'] = FileDataSerializer(instance.photo_uz, read_only=True).data
        representation['photo_ru'] = FileDataSerializer(instance.photo_ru, read_only=True).data
        representation['status'] = instance.status
        representation['status_display'] = instance.get_status_display()

        create_newsletter_task(instance.id, instance.send_date)
        return representation

    class Meta:
        model = Newsletter
        fields = ['id',
                  'send_date',
                  'bot_type',
                  'text_uz',
                  'text_ru',
                  'photo_uz',
                  'photo_ru', ]
