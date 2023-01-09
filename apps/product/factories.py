from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger
from faker import Faker

from apps.product.models import Category, Product

fake = Faker()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = fake.word()


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = SubFactory(CategoryFactory)
    name = fake.word()
    description = fake.sentence()
    price = FuzzyInteger(1, 1000)
    amount = FuzzyInteger(1, 50)
