from rest_framework import serializers, status

from apps.files.models import File
from apps.payment.models import Payment
from config.core.api_exceptions import APIValidation


class CustomerLoadPaymentSerializer(serializers.ModelSerializer):
    image = serializers.SlugRelatedField(source='files', slug_field='id', required=True, write_only=True,
                                         queryset=File.objects.all())

    def create(self, validated_data):
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
