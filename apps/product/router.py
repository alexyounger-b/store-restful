from rest_framework import routers

from apps.product.views import OrderViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register("order", OrderViewSet, basename="order")
router.register("product", ProductViewSet, basename="product")
