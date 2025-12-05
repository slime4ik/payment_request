from django.test import TestCase
from django.urls import reverse

from apps.request.models import PaymentRequest
from apps.request.tasks import check_request
from apps.request.models import PaymentRequest

class PaymentRequestTests(TestCase):

    def setUp(self):
        # Здесь можно подготовить данные, если нужно
        pass

    def test_create_payment_request_success(self):
        """
        Тест успешного создания заявки через модель напрямую
        """
        payout = PaymentRequest.objects.create(
            amount=100.00,
            currency="RUB",
            receiver_details="Test Receiver",
            comment="Test comment"
        )

        self.assertIsNotNone(payout.id)
        self.assertEqual(payout.status, PaymentRequest.StatusChoices.PENDING)

    def test_check_request_task_changes_status(self):
        """
        Тест ручного вызова Celery-задачи check_request
        """
        # Создаем заявку вручную
        payout = PaymentRequest.objects.create(
            amount=200.00,
            currency="RUB",
            receiver_details="Receiver Task Test",
            comment="Task test"
        )

        self.assertEqual(payout.status, PaymentRequest.StatusChoices.PENDING)

        check_request(str(payout.id))

        payout.refresh_from_db()
        self.assertEqual(payout.status, PaymentRequest.StatusChoices.SUCCESS)

