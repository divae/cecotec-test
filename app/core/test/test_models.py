
from django.test import TestCase
from django.contrib.auth import get_user_model


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
