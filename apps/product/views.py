from django.db.models import F
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response

from apps.product.exceptions import InsufficientFundsException
from apps.product.models import Order, Product
from apps.product.serializers import (
    OrderSerializer,
    ProductSerializer,
    ROOrderSerializer,
)


class ProductViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all().select_related("category")
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("status",)
    serializer_classes = {
        "create": OrderSerializer,
        "update": OrderSerializer,
        "partial_update": OrderSerializer,
        "retrieve": ROOrderSerializer,
        "list": ROOrderSerializer,
    }

    def get_serializer_context(self):
        """Extends current serializer context."""
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def get_serializer_class(self):
        """Get serializer base on action."""
        return self.serializer_classes.get(self.action) or super().get_serializer_class()

    def get_queryset(self):
        """Get orders only for requested user"""
        return super().get_queryset().filter(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="pay")
    def pay(self, request, pk):
        """Pay for the order."""
        user, order = request.user, self.get_object()
        if user.balance < order.product.price:
            raise InsufficientFundsException()

        user.balance = F("balance") - order.product.price
        user.save(update_fields=("balance",))
        order.status = Order.Status.PAID
        order.save(update_fields=("status",))
        return Response(status=status.HTTP_204_NO_CONTENT)
