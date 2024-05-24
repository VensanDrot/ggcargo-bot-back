from rest_framework import serializers

from config.core.choices import WAREHOUSE_CHOICE


class JWTLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TelegramLoginSerializer(serializers.Serializer):
    tg_id = serializers.CharField()
    warehouse = serializers.ChoiceField(choices=WAREHOUSE_CHOICE)

