
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from .models import Order, OrderLineItem
from products.models import Product


class CheckoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            description='Test description',
        )

    def test_checkout_view_GET(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_checkout_view_POST(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 200)  

    def test_checkout_view_empty_bag(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('checkout'))
        self.assertContains(response, "There's nothing in your bag at the moment")

class CheckoutSuccessViewTests(TestCase):
    def test_checkout_success_view_GET(self):
        response = self.client.get(reverse('checkout_success', args=['order_number']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')


class CacheCheckoutDataViewTests(TestCase):
    def test_cache_checkout_data_view_POST(self):
        response = self.client.post(reverse('cache_checkout_data'))
        self.assertEqual(response.status_code, 200) 


