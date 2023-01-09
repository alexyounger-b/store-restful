from django.db.models import F
from rest_framework import serializers

from apps.product.exceptions import ProductNotAvailableException
from apps.product.models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("category_name", "name", "description", "price", "amount")

    def get_category_name(self, instance):
        return getattr(instance.category, "name", "")


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    def validate_product(self, product):
        if product.amount <= 0:
            raise ProductNotAvailableException()
        return product

    class Meta:
        model = Order
        fields = ("status", "product", "user")
        extra_kwargs = {"user": {"required": False}}

    def validate(self, attrs):
        attrs["user"] = self.context["user"]
        return attrs

    def save(self, **kwargs):
        order = super().save(**kwargs)
        product = order.product
        product.amount = F("amount") - 1
        product.save(update_fields=("amount",))
        return order


class ROOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("status", "product_id", "user_id")
