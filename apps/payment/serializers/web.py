from django.utils.timezone import localdate
from rest_framework import serializers

from apps.files.serializer import FileDataSerializer
from apps.payment.models import Payment


class AdminPaymentOpenListSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField(allow_null=True)
    date = serializers.SerializerMethodField(allow_null=True)
    files = FileDataSerializer(many=True, allow_null=True)
    debt = serializers.FloatField(source='residue', allow_null=True)

    @staticmethod
    def get_date(obj):
        return localdate(obj.created_at)

    @staticmethod
    def get_customer_id(obj):
        return f'{obj.customer.prefix}{obj.customer.code}'

    class Meta:
        model = Payment
        fields = ['id',
                  'payment_card',
                  'customer_id',
                  'date',
                  'files',
                  'debt', ]


class AdminPaymentClosedListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', allow_null=True)
    customer_id = serializers.SerializerMethodField(allow_null=True)
    date = serializers.SerializerMethodField(allow_null=True)
    files = FileDataSerializer(many=True, allow_null=True)
    debt = serializers.FloatField(source='residue', allow_null=True)

    @staticmethod
    def get_date(obj):
        return localdate(obj.created_at)

    @staticmethod
    def get_customer_id(obj):
        return f'{obj.customer.prefix}{obj.customer.code}'

    class Meta:
        model = Payment
        fields = ['id',
                  'payment_card',
                  'customer_id',
                  'date',
                  'files',
                  'status',
                  'status_display',
                  'debt',
                  'paid_amount',
                  'comment', ]


class AdminPaymentApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id',
                  'paid_amount',
                  'comment', ]


class AdminPaymentDeclineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id',
                  'comment',
                  'paid_amount', ]
