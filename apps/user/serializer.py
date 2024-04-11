from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user.models import User, WEB_OR_TELEGRAM_CHOICE, WAREHOUSE_CHOICE, Operator


class JWTLoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['full_name'] = user.full_name
        return token


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ['tg_id',
                  'operator_type',
                  'warehouse',
                  'is_gg', ]


class GetUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.CharField(source='operators.first.tg_id')
    operator_type = serializers.ChoiceField(source='operators.first.get_operator_type_display',
                                            choices=WEB_OR_TELEGRAM_CHOICE)
    warehouse = serializers.ChoiceField(source='operators.first.get_warehouse_display', choices=WAREHOUSE_CHOICE)
    is_gg = serializers.BooleanField(source='operators.first.is_gg')

    class Meta:
        model = User
        depth = 1
        fields = ['id',
                  'full_name',
                  'email',
                  'tg_id',
                  'operator_type',
                  'warehouse',
                  'is_gg', ]


class PostUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.CharField(source='operators.tg_id', write_only=True, required=False)
    operator_type = serializers.ChoiceField(source='operators.operator_type', choices=WEB_OR_TELEGRAM_CHOICE,
                                            write_only=True, required=False)
    warehouse = serializers.ChoiceField(source='operators.warehouse', choices=WAREHOUSE_CHOICE, write_only=True,
                                        required=False)
    is_gg = serializers.BooleanField(source='operators.is_gg', write_only=True, required=False)

    def create(self, validated_data):
        operators = validated_data.pop('operators', {})
        user_password = validated_data.pop('password', None)
        user: User = super().create(validated_data)
        user.set_password(user_password)
        Operator.objects.create(user_id=user.id, **operators)
        user.save()
        return user

    def update(self, instance, validated_data):
        operators = validated_data.pop('operators', {})
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
                  'is_gg',
                  'full_name',
                  'email',
                  'password', ]
