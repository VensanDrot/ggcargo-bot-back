from rest_framework import serializers

from apps.user.models import User, WEB_OR_TELEGRAM_CHOICE, WAREHOUSE_CHOICE, Operator


class UserCreateSerializer(serializers.ModelSerializer):
    tg_id = serializers.CharField(source='operators.tg_id', write_only=True)
    operator_type = serializers.ChoiceField(source='operators.operator_type', choices=WEB_OR_TELEGRAM_CHOICE,
                                            write_only=True)
    warehouse = serializers.ChoiceField(source='operators.warehouse', choices=WAREHOUSE_CHOICE, write_only=True)
    is_gg = serializers.BooleanField(source='operators.is_gg', write_only=True)

    def create(self, validated_data):
        operators = validated_data.pop('operators', {})
        user_password = validated_data.pop('password', None)
        user: User = super().create(validated_data)
        user.set_password(user_password)
        Operator.objects.create(user_id=user.id, **operators)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['tg_id',
                  'operator_type',
                  'warehouse',
                  'is_gg',
                  'full_name',
                  'email',
                  'password', ]
