from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from uuid import uuid4


class User(AbstractUser):
    pass


# ============== Абстрактные Классы ==================


class BaseCreateClass(models.Model):
    """Абстрактный класс с полями id(uuid4), created_at, updated_at"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ^============== Абстрактные Классы ==================^


class PaymentRequest(BaseCreateClass):
    """Модель заявки платежа"""

    class CurrencyChoices(models.TextChoices):
        """Выбор валют RUB / USD / EUR"""

        RUB = "RUB", "Рубль"
        USD = "USD", "Доллар"
        EUR = "EUR", "Евро"

    class StatusChoices(models.TextChoices):
        """Статус платежа SUCCESS / PENDING / DECLINED"""

        SUCCESS = "SUCCESS", "Успешно"
        PENDING = "PENDING", "В ожидании"
        DECLINED = "DECLINED", "Отклонено"

    amount = models.DecimalField(  # Сумма
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    currency = models.CharField(  # Валюта
        max_length=3, choices=CurrencyChoices.choices, default=CurrencyChoices.RUB
    )
    receiver_details = models.CharField(  # Реквизиты получаителя(если есть)
        max_length=50, blank=True, null=True
    )
    status = models.CharField(  # Статус заявки
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    comment = models.CharField(max_length=500, blank=True, null=True) # Коментарий к заявке

    def __str__(self):
        return f"{self.amount} {self.currency}"
