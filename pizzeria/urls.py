from django.urls import path
from django.urls import path, include
from .views import OrderViewSet, OrderItemViewSet, OrderItemForItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="orders")
router.register("order_item", OrderItemViewSet, basename="order_item")
router.register("order_items", OrderItemForItemViewSet, basename="order_items")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/<int:pk>/", include(router.urls)),
]
