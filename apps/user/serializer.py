from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user.models import User, WEB_OR_TELEGRAM_CHOICE, WAREHOUSE_CHOICE, Operator, CAR_OR_AIR_CHOICE, Customer


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

    def create(self, validated_data):
        operators = validated_data.pop('operator', {})
        user_password = validated_data.pop('password', None)
        user: User = super().create(validated_data)
        user.set_password(user_password)
        Operator.objects.create(user_id=user.id, **operators)
        user.save()
        return user

    def update(self, instance, validated_data):
        operators = validated_data.pop('operator', {})
        user_password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        user.set_password(user_password)
        user.operators.update(**operators)
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


# TODO: end these
# CUSTOMERS
class GetCustomerSerializer(serializers.ModelSerializer):
    customer_code = serializers.CharField(source='customer.customer_code.code', read_only=True)
    user_type = serializers.ChoiceField(source='customer.get_user_type_display', choices=CAR_OR_AIR_CHOICE)
    phone_number = serializers.ChoiceField(source='customer.phone_number', choices=WAREHOUSE_CHOICE)

    class Meta:
        model = User
        depth = 1
        fields = ['id',
                  'full_name',
                  'email',
                  'customer_code',
                  'user_type',
                  'phone_number',
                  'is_active', ]


class PostCustomerSerializer(serializers.ModelSerializer):
    customer_code = serializers.CharField(source='customer.code', read_only=True)
    user_type = serializers.ChoiceField(source='customer.user_type', choices=CAR_OR_AIR_CHOICE)
    phone_number = serializers.ChoiceField(source='customer.phone_number', choices=WAREHOUSE_CHOICE)
    def create(self, validated_data):
        operators = validated_data.pop('customer', {})
        user_password = validated_data.pop('password', None)
        user: User = super().create(validated_data)
        user.set_password(user_password)
        Customer.objects.create(user_id=user.id, **operators)
        user.save()
        return user

    def update(self, instance, validated_data):
        operators = validated_data.pop('customer', {})
        user_password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        user.set_password(user_password)
        user.operators.update(**operators)
        user.save()
        return instance

    class Meta:
        model = User
        fields = ['customer_code',
                  'user_type',
                  'phone_number',
                  'full_name',
                  'email',
                  'password', ]
