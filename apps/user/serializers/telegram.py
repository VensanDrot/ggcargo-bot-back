from rest_framework import serializers, status
from django.utils.translation import gettext_lazy as _

from apps.files.models import File
from apps.loads.models import Product
from apps.user.models import User, Customer, CustomerRegistration
from apps.user.utils.services import generate_code
from config.core.api_exceptions import APIValidation


class CustomerAviaRegistrationStepOneSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='customer.language', required=False)
    phone_number = serializers.CharField(source='customer.phone_number', required=True)
    tg_id = serializers.CharField(source='customer.tg_id', required=True)
    password = serializers.CharField(write_only=True, required=True)
    customer_id = serializers.SerializerMethodField(allow_null=True, read_only=True)

    @staticmethod
    def get_customer_id(obj):
        return f"{obj.customer.prefix}{obj.customer.code}"

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        customer_data = validated_data.pop('customer', {})
        existing_customer = Customer.objects.filter(phone_number=customer_data.get('phone_number'), user_type='AVIA',
                                                    prefix__isnull=False, code__isnull=False)
        if existing_customer.exists():
            if not existing_customer.first().customer_registrations.filter(done=False).exists():
                raise APIValidation('Customer with this phone number already exists',
                                    status_code=status.HTTP_400_BAD_REQUEST)
        if existing_customer.exists():
            existing_customer = existing_customer.first()
            customer_registration = existing_customer.customer_registrations.filter(done=False)
            if customer_registration:
                customer_registration = customer_registration.first()
                customer_registration.step = 1
                customer_registration.save()
            else:
                CustomerRegistration.objects.create(customer=existing_customer, step=1)
            instance = existing_customer.user
            instance.full_name = validated_data.get('full_name')
            instance.set_password(password)
            instance.save()
            return instance
        instance = super().create(validated_data)
        deleted_customer = Customer.objects.filter(prefix='DELETE', is_data_transferred=False)
        if deleted_customer.exists():
            deleted_customer = deleted_customer.first()
            prefix, code = deleted_customer.ex_prefix, deleted_customer.ex_code
            transferred_customer_products = deleted_customer.products.filter(status='DONE')
            transferred_customer_loads = deleted_customer.loads.filter(status__in=['DONE', 'DONE_MAIL'])
            other_products = deleted_customer.products.filter(status__in=['ON_WAY', 'DELIVERED', ])
            customer = Customer.objects.create(user_id=instance.id, prefix=prefix, code=code,
                                               user_type='AVIA', **customer_data)
            transferred_customer_products.update(customer_id=customer.id)
            transferred_customer_loads.update(customer_id=customer.id)
            other_products.update(customer_id=None, is_homeless=True)
            deleted_customer.is_data_transferred = True
            deleted_customer.save()
        else:
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
                  'tg_id',
                  'language',
                  'full_name',
                  'phone_number',
                  'password',
                  'customer_id', ]


class CustomerAviaRegistrationStepTwoSerializer(serializers.ModelSerializer):
    passport_photo = serializers.SlugRelatedField(source='customer.passport_photo', slug_field='id', required=True,
                                                  write_only=True, queryset=File.objects.all())
    birth_date = serializers.DateField(source='customer.birth_date')
    passport_serial_number = serializers.CharField(source='customer.passport_serial_number')

    def update(self, instance, validated_data):
        registration_app = instance.customer.customer_registrations.filter(status='WAITING').first()
        if registration_app.step > 1:
            raise APIValidation(_('Этот шаг регистрации уже выполнен.'),
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
        registration_app: CustomerRegistration = instance.customer.customer_registrations.filter(
            status='WAITING').first()
        if registration_app.step > 2:
            raise APIValidation('Registration was already done, wait operators response',
                                status_code=status.HTTP_400_BAD_REQUEST)
        customer_data = validated_data.pop('customer', {})
        instance = super().update(instance, validated_data)
        registration_app.files.add(*customer_data['files'])
        registration_app.step = 3
        registration_app.done = True
        registration_app.save()
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'files', ]


class CustomerAutoRegistrationStepOneSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='customer.language', required=False)
    phone_number = serializers.CharField(source='customer.phone_number', required=True)
    tg_id = serializers.CharField(source='customer.tg_id', required=True)
    password = serializers.CharField(write_only=True, required=True)
    customer_id = serializers.SerializerMethodField(allow_null=True, read_only=True)

    @staticmethod
    def get_customer_id(obj):
        return f"{obj.customer.prefix}{obj.customer.code}"

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        customer_data = validated_data.pop('customer', {})
        existing_customer = Customer.objects.filter(phone_number=customer_data.get('phone_number'), user_type='AUTO')
        if existing_customer.exists():
            if not existing_customer.first().customer_registrations.filter(done=False).exists():
                raise APIValidation('Customer with this phone number already exists',
                                    status_code=status.HTTP_400_BAD_REQUEST)
        if existing_customer.exists():
            existing_customer = existing_customer.first()
            customer_registration = existing_customer.customer_registrations.filter(done=False)
            if customer_registration:
                customer_registration = customer_registration.first()
                customer_registration.step = 1
                customer_registration.save()
            else:
                CustomerRegistration.objects.create(customer=existing_customer, step=1)
            instance = existing_customer.user
            instance.full_name = validated_data.get('full_name')
            instance.set_password(password)
            instance.save()
            return instance
        instance = super().create(validated_data)
        deleted_customer = Customer.objects.filter(prefix='DELETE', is_data_transferred=False)
        if deleted_customer.exists():
            deleted_customer = deleted_customer.first()
            prefix, code = deleted_customer.ex_prefix, deleted_customer.ex_code
            transferred_customer_products = deleted_customer.products.filter(status='DONE')
            transferred_customer_loads = deleted_customer.loads.filter(status__in=['DONE', 'DONE_MAIL'])
            other_products = deleted_customer.products.filter(status__in=['ON_WAY', 'DELIVERED', ])
            customer = Customer.objects.create(user_id=instance.id, prefix=prefix, code=code,
                                               user_type='AUTO', **customer_data)
            transferred_customer_products.update(customer_id=customer.id)
            transferred_customer_loads.update(customer_id=customer.id)
            other_products.update(customer_id=None, is_homeless=True)
            deleted_customer.is_data_transferred = True
            deleted_customer.save()
        else:
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
                  'tg_id',
                  'language',
                  'full_name',
                  'phone_number',
                  'password',
                  'customer_id', ]


class CustomerAutoRegistrationStepTwoSerializer(serializers.ModelSerializer):
    files = serializers.SlugRelatedField(source='customer.files', slug_field='id', many=True,
                                         queryset=File.objects.all(), required=False)

    def update(self, instance, validated_data):
        registration_app: CustomerRegistration = instance.customer.customer_registrations.filter(
            status='WAITING').first()
        if registration_app.step > 2:
            raise APIValidation('Registration was already done, wait operators response',
                                status_code=status.HTTP_400_BAD_REQUEST)
        customer_data = validated_data.pop('customer', {})
        instance = super().update(instance, validated_data)
        registration_app.files.add(*customer_data['files'])
        registration_app.step = 3
        registration_app.done = True
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
