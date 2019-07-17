from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product, Order

from product.serializers import ProductSerializer


PRODUCT_URL = reverse('product:product-list')


class PublicProductsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductsApiTests(TestCase):
    """Test the authorized user product API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_product(self):
        Product.objects.create(
            user=self.user,
            price=2.22,
            name='Sandalia'
            )
        Product.objects.create(
            user=self.user,
            price=2.22,
            name='Tacón')

        res = self.client.get(PRODUCT_URL)

        products = Product.objects.all().order_by('-name')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_products_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'other@test.com',
            'testpass'
        )
        Product.objects.create(
            user=user2,
            price=2.22,
            name='Sandalia')
        product = Product.objects.create(
            user=self.user,
            price=2.22,
            name='Tacon')

        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], product.name)

    def test_create_product_invalid(self):
        payload = {'name': ''}
        res = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_products_assigned_to_orders(self):
        product1 = Product.objects.create(
            user=self.user,
            price=2.22,
            name='Sandalia')
        product2 = Product.objects.create(
            user=self.user,
            price=2.22,
            name='Tacon')
        order = Order.objects.create(
            name='My order',
            user=self.user,
            number=1
        )
        order.products.add(product1)

        res = self.client.get(PRODUCT_URL, {'assigned_only': 1})

        serializer1 = ProductSerializer(product1)
        serializer2 = ProductSerializer(product2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_products_assigned_unique(self):
        product = Product.objects.create(
            user=self.user,
            price=2.22,
            name='Tacón')
        order1 = Order.objects.create(
            name='My order',
            user=self.user,
            number=1
        )
        order1.products.add(product)
        order2 = Order.objects.create(
            name='My order2',
            user=self.user,
            number=2
        )
        order2.products.add(product)

        res = self.client.get(PRODUCT_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
