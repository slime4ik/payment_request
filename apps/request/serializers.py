from rest_framework import serializers
from .models import PaymentRequest


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки платежа"""

    class Meta:
        model = PaymentRequest
        fields = (
            "amount",
            "currency",
            "receiver_details",
            "comment",
        )

    def validate_amount(self, value):
        """Валидация суммы: должна быть > 0 и не слишком большой"""
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть больше нуля.")

        if value > 10_000_000:
            raise serializers.ValidationError("Сумма слишком большая.")

        return value

    def validate_receiver_details(self, value):
        """Валидация реквизитов"""
        if value and len(value) < 5:
            raise serializers.ValidationError(
                "Реквизиты слишком короткие — минимум 5 символов."
            )
        return value


class PaymentSerializer(serializers.ModelSerializer):
    """Полная информация о платёжной заявке"""
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    class Meta:
        model = PaymentRequest
        fields = (
            "id",
            "amount",
            "currency",
            "receiver_details",
            "status",
            "comment",
            "created_at",
            "updated_at",
        )


class PaymentRequestPatchSerializer(serializers.ModelSerializer):
    """PATCH — частичное обновление (в основном — статуса)"""

    class Meta:
        model = PaymentRequest
        fields = ["status"]