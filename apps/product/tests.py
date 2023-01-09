from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.authentication.models import User
from apps.product.factories import ProductFactory
from apps.product.models import Order


class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@ex.com", password="Qwerty@123")
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_retrieve(self):
        product = ProductFactory.create()
        url = reverse("product-detail", args=(product.id,))
        r = self.client.get(url, HTTP_AUTHORIZATION=f"Token {self.token}")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["category_name"], product.category.name)
        self.assertEqual(r.data["name"], product.name)

    def test_list(self):
        ProductFactory.create()
        ProductFactory.create()
        ProductFactory.create()

        url = reverse("product-list")
        r = self.client.get(url, HTTP_AUTHORIZATION=f"Token {self.token}")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 3)


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@ex.com", password="Qwerty@123")
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_create(self):
        url = reverse("order-list")
        product = ProductFactory.create()

        # Out of stock
        product.amount = 0
        product.save(update_fields=("amount",))
        r = self.client.post(url, {"product": product.id}, HTTP_AUTHORIZATION=f"Token {self.token}")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.data["detail"], "The product out of stock.")

        # Success
        product.amount = 5
        product.save(update_fields=("amount",))
        r = self.client.post(url, {"product": product.id}, HTTP_AUTHORIZATION=f"Token {self.token}")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data["user"], self.user.id)
        self.assertEqual(r.data["product"], product.id)
        product.refresh_from_db()
        self.assertEqual(product.amount, 4)

    def test_list(self):
        url = reverse("order-list")
        product = ProductFactory.create(amount=5)
        another_user = User.objects.create_user("another_user@ex.com", "Qwerty@123")

        Order.objects.create(user=self.user, product=product)
        Order.objects.create(user=self.user, product=product)
        Order.objects.create(user=another_user, product=product)
        r = self.client.get(url, HTTP_AUTHORIZATION=f"Token {self.token}")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 2)

    def test_pay(self):
        product = ProductFactory.create(price=20)
        order = Order.objects.create(user=self.user, product=product)

        # Insufficient funds
        url = reverse("order-pay", args=(order.id,))
        r = self.client.post(url, HTTP_AUTHORIZATION=f"Token {self.token}")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.data["detail"], "Insufficient funds.")

        # Success
        self.user.balance = 50
        self.user.save(update_fields=("balance",))
        r = self.client.post(url, HTTP_AUTHORIZATION=f"Token {self.token}")
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 30)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAID)
