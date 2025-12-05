from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'request'

router = DefaultRouter()
router.register(r'requests', views.PaymentRequestViewSet, basename='requests')

urlpatterns = [
    path('', include(router.urls)),
]