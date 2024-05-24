from rest_framework import serializers, status
from django.utils.translation import gettext_lazy as _

from apps.files.models import File
from apps.loads.models import Product
from apps.user.models import User, Customer, CustomerRegistration
from apps.user.utils.services import generate_code
from config.core.api_exceptions import APIValidation


class CustomerAviaRegistrationStepOneSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='customer.phone_number', required=True)
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        customer_data = validated_data.pop('customer', {})
        instance = super().create(validated_data)
        prefix, code = generate_code({'user_type': 'AVIA'})
        customer = Customer.objects.create(user_id=instance.id, prefix=prefix, code=code,
                                           user_type='AVIA', **customer_data)
        instance.customer_id = customer.id
        instance.is_active = False
        instance.set_password(password)
        instance.save()
        CustomerRegistration.objects.create(customer=customer, step=1)
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'full_name',
                  'phone_number',
                  'password', ]


class CustomerAviaRegistrationStepTwoSerializer(serializers.ModelSerializer):
    passport_photo = serializers.SlugRelatedField(source='customer.passport_photo', slug_field='id', required=True,
                                                  write_only=True, queryset=File.objects.all())
    birth_date = serializers.DateField(source='customer.birth_date')
    passport_serial_number = serializers.CharField(source='customer.passport_serial_number')

    def update(self, instance, validated_data):
        registration_app = instance.customer.customer_registrations.filter(status=None).first()
        if registration_app.step > 1:
            raise APIValidation(_('This step of registration has been already done'),
                                status_code=status.HTTP_400_BAD_REQUEST)
        customer_data = validated_data.pop('customer', {})
        instance = super().update(instance, validated_data)
        for key, value in customer_data.items():
            setattr(instance.customer, key, value)
        instance.customer.save()
        registration_app.step = 2
        registration_app.save()
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'birth_date',
                  'passport_serial_number',
                  'passport_photo', ]


class CustomerAviaRegistrationStepThreeSerializer(serializers.ModelSerializer):
    files = serializers.SlugRelatedField(source='customer.files', slug_field='id', many=True,
                                         queryset=File.objects.all(), required=False)

    def update(self, instance, validated_data):
        registration_app: CustomerRegistration = instance.customer.customer_registrations.filter(status=None).first()
        if registration_app.step > 2:
            raise APIValidation('Registration was already done, wait operators response',
                                status_code=status.HTTP_400_BAD_REQUEST)
        customer_data = validated_data.pop('customer', {})
        instance = super().update(instance, validated_data)
        registration_app.files.add(*customer_data['files'])
        registration_app.step = 3
        registration_app.save()
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'files', ]


class CustomerAutoRegistrationStepOneSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='customer.phone_number', required=True)
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        customer_data = validated_data.pop('customer', {})
        instance = super().create(validated_data)
        prefix, code = generate_code({'user_type': 'AUTO'})
        customer = Customer.objects.create(user_id=instance.id, prefix=prefix, code=code,
                                           user_type='AUTO', **customer_data)
        instance.customer_id = customer.id
        instance.is_active = False
        instance.set_password(password)
        instance.save()
        CustomerRegistration.objects.create(customer=customer, step=1)
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'full_name',
                  'phone_number',
                  'password', ]


class CustomerAutoRegistrationStepTwoSerializer(serializers.ModelSerializer):
    files = serializers.SlugRelatedField(source='customer.files', slug_field='id', many=True,
                                         queryset=File.objects.all(), required=False)

    def update(self, instance, validated_data):
        registration_app: CustomerRegistration = instance.customer.customer_registrations.filter(status=None).first()
        if registration_app.step > 2:
            raise APIValidation('Registration was already done, wait operators response',
                                status_code=status.HTTP_400_BAD_REQUEST)
        customer_data = validated_data.pop('customer', {})
        instance = super().update(instance, validated_data)
        registration_app.files.add(*customer_data['files'])
        registration_app.step = 3
        registration_app.save()
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'files', ]


class CustomerSettingsPersonalRetrieveSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='customer.phone_number', read_only=True)
    language = serializers.CharField(source='customer.language', read_only=True)

    class Meta:
        model = User
        fields = ['id',
                  'full_name',
                  'phone_number',
                  'language', ]


class CustomerSettingsPersonalUpdateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='customer.phone_number')
    language = serializers.CharField(source='customer.language')

    def update(self, instance, validated_data):
        customer_data = validated_data.pop('customer', {})
        instance = super().update(instance, validated_data)
        customer = instance.customer
        customer.language = customer_data.get('language', customer.language)
        customer.phone_number = customer_data.get('phone_number', customer.phone_number)
        customer.save()
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'phone_number',
                  'language', ]


class CustomerSettingsPasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    def update(self, instance: User, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'password', ]
