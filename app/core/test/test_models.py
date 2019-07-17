
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@test.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'stlmedrano@gmail.com'
        password = 'test123'

        user = sample_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'stlmedrano@GMAIL.com'
        test_password = 'test123'
        user = get_user_model().objects.create_user(email, test_password)

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        test_password = 'test123'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, test_password)

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'sfs@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_product_str(self):
        product = models.Product.objects.create(
            user=sample_user(),
            name='My product',
            price=5.00
        )

        self.assertEqual(str(product), product.name)

    def test_order_str(self):
        order = models.Order.objects.create(
            name='My order',
            user=sample_user(),
            number=1
        )

        self.assertEqual(str(order), order.name)
