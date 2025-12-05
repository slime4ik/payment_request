import uuid
from celery import shared_task
from django.db import transaction

# Локальные импорты
from .models import PaymentRequest

import logging

logger = logging.getLogger(__name__)


@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def check_request(request_id) -> None:
    """Моковая задача которая меняет статус заявки на SUCCESS"""

    try:
        with transaction.atomic():
            payout_id = uuid.UUID(str(request_id))
            payment = PaymentRequest.objects.select_for_update().get(
                id=(payout_id)
            )

            payment.status = PaymentRequest.StatusChoices.SUCCESS
            payment.save()

    except Exception as e:
        logger.error(f"Ошибка проверки заявки {request_id}: {e}")
        raise
