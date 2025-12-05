from http import HTTPStatus
import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import PaymentRequest
from .serializers import (
    PaymentCreateSerializer,
    PaymentSerializer,
    PaymentRequestPatchSerializer,
)
from .services import PaymentRequestService

logger = logging.getLogger(__name__)


class PaymentRequestViewSet(viewsets.ViewSet):

    # -------------------------------------------------
    # GET /api/payouts/ — список заявок
    # -------------------------------------------------
    @extend_schema(
        responses={200: PaymentSerializer(many=True)},
        summary="Список заявок",
        description="Возвращает список всех платёжных заявок с пагинацией",
    )
    def list(self, request: Request) -> Response:
        queryset = PaymentRequest.objects.all().order_by("-created_at")
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = PaymentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # -------------------------------------------------
    # GET /api/payouts/{id}/ — одна заявка
    # -------------------------------------------------
    @extend_schema(
        responses={200: PaymentSerializer},
        summary="Получить заявку по ID",
        description="Возвращает одну заявку по UUID",
    )
    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        try:
            payout = PaymentRequest.objects.get(id=pk)
        except PaymentRequest.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PaymentSerializer(payout)
        return Response(serializer.data)

    # -------------------------------------------------
    # POST /api/payouts/ — создать заявку
    # -------------------------------------------------
    @extend_schema(
        request=PaymentCreateSerializer,
        responses={201: PaymentSerializer},
        summary="Создать новую заявку",
        description="Создаёт платёжную заявку",
    )
    def create(self, request: Request) -> Response:
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payout, error = PaymentRequestService.create_request(serializer.validated_data)

        if payout is None:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PaymentSerializer(payout).data, status=status.HTTP_201_CREATED)

    # -------------------------------------------------
    # PATCH /api/payouts/{id}/ — частичное обновление
    # -------------------------------------------------
    @extend_schema(
        request=PaymentRequestPatchSerializer,
        responses={200: PaymentSerializer},
        summary="Обновить заявку (частично)",
        description="Частичное обновление заявки, например, смена статуса",
    )
    def partial_update(self, request: Request, pk: str | None = None) -> Response:
        try:
            payout = PaymentRequest.objects.get(id=pk)
        except PaymentRequest.DoesNotExist:
            return Response({"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentRequestPatchSerializer(payout, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(PaymentSerializer(payout).data)

    # -------------------------------------------------
    # DELETE /api/payouts/{id}/ — удалить заявку
    # -------------------------------------------------
    @extend_schema(
        responses={204: None},
        summary="Удалить заявку",
        description="Удаляет заявку по ID",
    )
    def destroy(self, request: Request, pk: str | None = None) -> Response:
        try:
            payout = PaymentRequest.objects.get(id=pk)
        except PaymentRequest.DoesNotExist:
            return Response({"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND)

        payout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
