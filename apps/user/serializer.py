from datetime import datetime

from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.files.models import File
from apps.user.models import User, Operator, Customer
from apps.user.utils.choices import WEB_OR_TELEGRAM_CHOICE, WAREHOUSE_CHOICE, CAR_OR_AIR_CHOICE, PREFIX_CHOICES

from apps.user.utils.services import generate_customer_code, prefix_check
from config.core.api_exceptions import APIValidation


class JWTLoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['full_name'] = user.full_name
        return token


# STAFF
class GetUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.CharField(source='operator.tg_id')
    operator_type = serializers.ChoiceField(source='operator.get_operator_type_display',
                                            choices=WEB_OR_TELEGRAM_CHOICE)
    warehouse = serializers.ChoiceField(source='operator.get_warehouse_display', choices=WAREHOUSE_CHOICE)
    company_type = serializers.CharField(source='get_company_type_display')

    class Meta:
        model = User
        depth = 1
        fields = ['id',
                  'full_name',
                  'email',
                  'tg_id',
                  'operator_type',
                  'warehouse',
                  'company_type', ]


class PostUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.CharField(source='operator.tg_id', write_only=True, required=False)
    operator_type = serializers.ChoiceField(source='operator.operator_type', choices=WEB_OR_TELEGRAM_CHOICE,
                                            write_only=True, required=False)
    warehouse = serializers.ChoiceField(source='operator.warehouse', choices=WAREHOUSE_CHOICE, write_only=True,
                                        required=False)

    def validate_warehouse(self, value):
        user = self.context['request'].user
        if user.is_superuser:
            return value
        if user.operator.warehouse != value:
            raise APIValidation('Warehouse is incorrect', status_code=status.HTTP_400_BAD_REQUEST)
        return value

    def validate_company_type(self, value):
        user = self.context.get('request').user
        if user.is_superuser:
            return value
        if user.company_type != value:
            raise APIValidation('Company type is invalid', status_code=status.HTTP_400_BAD_REQUEST)
        return value

    def create(self, validated_data):
        operators = validated_data.pop('operator', {})
        user_password = validated_data.pop('password', None)
        user: User = super().create(validated_data)
        user.set_password(user_password)
        Operator.objects.create(user_id=user.id, **operators)
        user.save()
        return user

    def update(self, instance, validated_data):
        operator = validated_data.pop('operator', {})
        user_password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        user.set_password(user_password)
        user.operator.update(**operator)
        user.save()
        return instance

    class Meta:
        model = User
        fields = ['tg_id',
                  'operator_type',
                  'warehouse',
                  'company_type',
                  'full_name',
                  'email',
                  'password', ]


# CUSTOMERS
class GetCustomerSerializer(serializers.ModelSerializer):
    customer_code = serializers.CharField(source='customer.code', allow_null=True)
    user_type = serializers.ChoiceField(source='customer.get_user_type_display', choices=CAR_OR_AIR_CHOICE)
    phone_number = serializers.ChoiceField(source='customer.phone_number', choices=WAREHOUSE_CHOICE)
    accepted_by = serializers.CharField(source='customer.accepted_by.full_name', allow_null=True)

    class Meta:
        model = User
        depth = 1
        fields = ['id',
                  'full_name',
                  'customer_code',
                  'user_type',
                  'company_type',
                  'phone_number',
                  'accepted_by',
                  'is_active', ]


class PostCustomerSerializer(serializers.ModelSerializer):
    prefix = serializers.ChoiceField(source='customer.prefix', allow_null=True, required=False, choices=PREFIX_CHOICES)
    customer_id = serializers.CharField(source='customer.code')
    user_type = serializers.ChoiceField(source='customer.user_type', choices=CAR_OR_AIR_CHOICE)
    phone_number = serializers.CharField(source='customer.phone_number')
    current_password = serializers.CharField(allow_null=True, required=False)
    passport_photo = serializers.PrimaryKeyRelatedField(source='customer.passport_photo', required=False,
                                                        queryset=File.objects.all())
    birt_date = serializers.DateField(source='customer.birt_date', required=False)
    passport_serial_number = serializers.CharField(source='customer.passport_serial_number', required=False)

    def validate_customer_id(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Code should be a number")
        return value.zfill(4)

    def create(self, validated_data: dict):
        try:
            validated_data.pop('current_password', None)
            user_password = validated_data.pop('password', None)

            request = self.context.get('request')
            customer_data = validated_data.pop('customer', {})
            prefix_check(customer_data.get('prefix'), customer_data.get('user_type'), request)

            user = super().create(validated_data)
            if not validated_data.get('company_type'):
                user.company_type = request.user.company_type
            user.set_password(user_password)
            user.save()

            Customer.objects.create(user=user, accepted_time=datetime.now(), accepted_by=request.user, **customer_data)
            return user
        except Exception as exc:
            if 'user' in locals() and user:
                user.delete()
            raise APIValidation(f"{exc.args}", status_code=status.HTTP_400_BAD_REQUEST)

    def update(self, instance: User, validated_data: dict):
        try:
            current_password = validated_data.pop('current_password', None)
            user_password = validated_data.pop('password', None)

            request = self.context.get('request')
            customer_data = validated_data.pop('customer', {})
            prefix_check(customer_data.get('prefix'), customer_data.get('user_type'), request)

            if current_password and not instance.check_password(current_password):
                raise serializers.ValidationError("Current password is incorrect")

            user = super().update(instance, validated_data)
            if user_password:
                user.set_password(user_password)
                user.save()

            Customer.objects.filter(user=user, accepted_by=request.user).update(**customer_data)
            return instance
        except Exception as exc:
            raise APIValidation(f"{exc.args}", status_code=status.HTTP_400_BAD_REQUEST)

    class Meta:
        model = User
        fields = ['prefix',
                  'customer_id',
                  'user_type',
                  'company_type',
                  'phone_number',
                  'full_name',
                  'password',
                  'current_password',
                  'is_active',
                  'passport_photo',
                  'birt_date',
                  'passport_serial_number', ]
