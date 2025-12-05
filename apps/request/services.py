from typing import Tuple, Optional
# Локальные импорты
from .models import PaymentRequest
from .tasks import check_request

import logging
logger = logging.getLogger(__name__)

class PaymentRequestService:
    """Сервис для управления заявками на платежи"""
    @staticmethod
    def create_request(validated_data) -> Tuple[Optional[PaymentRequest], Optional[str]]:
        """Создание заявки"""
        try:
            payment_request = PaymentRequest.objects.create(**validated_data)
            logger.info(f"Заявка успешно создана: {validated_data}")
            check_request.delay(payment_request.id)
            return payment_request, None
        except Exception as e:
            logger.error(f"Ошибка создания заявки: {validated_data}")
            return None, str(e)
