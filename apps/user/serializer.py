from datetime import datetime

from rest_framework import serializers, status

from apps.files.models import File
from apps.files.serializer import FileDataSerializer
from apps.user.models import User, Operator, Customer
from apps.user.utils.choices import WEB_OR_TELEGRAM_CHOICE, WAREHOUSE_CHOICE, CAR_OR_AIR_CHOICE, PREFIX_CHOICES

from apps.user.utils.services import generate_code
from config.core.api_exceptions import APIValidation


class JWTLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TelegramLoginSerializer(serializers.Serializer):
    tg_id = serializers.CharField()
    warehouse = serializers.ChoiceField(choices=WAREHOUSE_CHOICE)


# STAFF
class GetUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.CharField(source='operator.tg_id')
    operator_type = serializers.ChoiceField(source='operator.get_operator_type_display',
                                            choices=WEB_OR_TELEGRAM_CHOICE)
    warehouse = serializers.ChoiceField(source='operator.get_warehouse_display', choices=WAREHOUSE_CHOICE)

    # company_type = serializers.CharField(source='get_company_type_display')

    class Meta:
        model = User
        depth = 1
        fields = [
            'id',
            'full_name',
            'email',
            'tg_id',
            'operator_type',
            'warehouse',
            # 'company_type',
        ]


class PostUserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(source='operator.is_admin', write_only=True, required=False)
    tg_id = serializers.CharField(source='operator.tg_id', write_only=True, required=False)
    operator_type = serializers.ChoiceField(source='operator.operator_type', choices=WEB_OR_TELEGRAM_CHOICE,
                                            write_only=True, required=False)
    warehouse = serializers.ChoiceField(source='operator.warehouse', choices=WAREHOUSE_CHOICE, write_only=True,
                                        required=False)

    def validate_warehouse(self, value):
        user = self.context['request'].user
        if user.is_superuser:
            return value
        if not user.operator.is_admin:
            raise APIValidation('Operator is not admin', status_code=status.HTTP_403_FORBIDDEN)
        elif user.operator.warehouse != value:
            raise APIValidation('Warehouse is incorrect', status_code=status.HTTP_400_BAD_REQUEST)
        return value

    # def validate_company_type(self, value):
    #     user = self.context.get('request').user
    #     if user.is_superuser:
    #         return value
    #     if user.company_type != value:
    #         raise APIValidation('Company type is invalid', status_code=status.HTTP_400_BAD_REQUEST)
    #     return value

    def create(self, validated_data):
        operators = validated_data.pop('operator', {})
        user_password = validated_data.pop('password', None)
        user: User = super().create(validated_data)
        user.set_password(user_password)
        Operator.objects.create(user_id=user.id, **operators)
        user.save()
        return user

    def update(self, instance, validated_data):
        operator_data = validated_data.pop('operator', {})
        user_password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        user.set_password(user_password)
        for key, value in operator_data.items():
            setattr(user.operator, key, value)
        user.operator.save()
        user.save()
        return instance

    class Meta:
        model = User
        fields = ['id',
                  'tg_id',
                  'operator_type',
                  'warehouse',
                  # 'company_type',
                  'full_name',
                  'email',
                  'password',
                  'is_admin', ]


# CUSTOMERS
class GetCustomerSerializer(serializers.ModelSerializer):
    debt = serializers.CharField(source='customer.debt', allow_null=True)
    customer_code = serializers.SerializerMethodField(allow_null=True)
    user_type = serializers.ChoiceField(source='customer.get_user_type_display', choices=CAR_OR_AIR_CHOICE)
    phone_number = serializers.ChoiceField(source='customer.phone_number', choices=WAREHOUSE_CHOICE)
    accepted_by = serializers.CharField(source='customer.accepted_by.full_name', allow_null=True)

    @staticmethod
    def get_customer_code(obj):
        customer = obj.customer
        return f'{customer.prefix}{customer.code}'

    class Meta:
        model = User
        depth = 1
        fields = ['id',
                  'full_name',
                  'customer_code',
                  'user_type',
                  # 'company_type',
                  'phone_number',
                  'debt',
                  'accepted_by',
                  'is_active', ]


class RetrieveCustomerSerializer(serializers.ModelSerializer):
    debt = serializers.CharField(source='customer.debt', allow_null=True)
    prefix = serializers.CharField(source='customer.prefix', allow_null=True)
    code = serializers.CharField(source='customer.code', allow_null=True)
    user_type = serializers.ChoiceField(source='customer.get_user_type_display', choices=CAR_OR_AIR_CHOICE)
    phone_number = serializers.ChoiceField(source='customer.phone_number', choices=WAREHOUSE_CHOICE)
    passport_photo = FileDataSerializer(source='customer.passport_photo')
    birth_date = serializers.CharField(source='customer.birth_date')
    passport_serial_number = serializers.CharField(source='customer.passport_serial_number')
    accepted_by = serializers.CharField(source='customer.accepted_by.full_name', allow_null=True)

    class Meta:
        model = User
        depth = 1
        fields = ['id',
                  'full_name',
                  'prefix',
                  'code',
                  'user_type',
                  # 'company_type',
                  'phone_number',
                  'passport_photo',
                  'birth_date',
                  'passport_serial_number',
                  'debt',
                  'accepted_by',
                  'is_active', ]


class PostCustomerSerializer(serializers.ModelSerializer):
    # prefix = serializers.ChoiceField(source='customer.prefix', allow_null=True, required=False,
    # choices=PREFIX_CHOICES)
    # customer_id = serializers.CharField(source='customer.code', allow_null=True, required=False)
    user_type = serializers.ChoiceField(source='customer.user_type', choices=CAR_OR_AIR_CHOICE, allow_null=True,
                                        required=False)
    phone_number = serializers.CharField(source='customer.phone_number', allow_null=True, required=False)
    passport_photo = serializers.PrimaryKeyRelatedField(source='customer.passport_photo', required=False,
                                                        queryset=File.objects.all(), allow_null=True)
    birth_date = serializers.DateField(source='customer.birth_date', required=False, allow_null=True)
    passport_serial_number = serializers.CharField(source='customer.passport_serial_number', required=False,
                                                   allow_null=True)

    def validate_customer_id(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Code should be a number")
        return value.zfill(4)

    def create(self, validated_data: dict):
        try:
            user_password = validated_data.pop('password', None)

            request = self.context.get('request')
            customer_data = validated_data.pop('customer', {})
            prefix, code = generate_code(customer_data)

            user = super().create(validated_data)
            user.set_password(user_password)
            user.save()

            Customer.objects.create(user=user, prefix=prefix, code=code, accepted_time=datetime.now(),
                                    accepted_by=request.user, **customer_data)
            return user
        except Exception as exc:
            if 'user' in locals() and user:
                user.delete()
            raise APIValidation(f"{exc.args}", status_code=status.HTTP_400_BAD_REQUEST)

    def update(self, instance: User, validated_data: dict):
        try:
            user_password = validated_data.pop('password', None)

            request = self.context.get('request')
            customer_data = validated_data.pop('customer', {})

            user = super().update(instance, validated_data)
            if user_password:
                user.set_password(user_password)
                user.save()

            Customer.objects.filter(user=user).update(accepted_by=request.user, **customer_data)
            return instance
        except Exception as exc:
            raise APIValidation(f"{exc.args}", status_code=status.HTTP_400_BAD_REQUEST)

    class Meta:
        model = User
        fields = [
            'id',
            # 'prefix',
            # 'customer_id',
            'user_type',
            # 'company_type',
            'phone_number',
            'full_name',
            'password',
            # 'current_password',
            'is_active',
            'passport_photo',
            'birth_date',
            'passport_serial_number',
        ]
