from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile
from checkout.models import Order

class ProfileViewTests(TestCase):
    
    def setUpTestData(cls):
        # Set up test data, including creating a user and a user profile if needed.
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        cls.profile = UserProfile.objects.create(
            user=cls.user,
            default_phone_number='1234567890',
            default_country='US',
            default_postcode='12345',
            default_town_or_city='Test City',
            default_street_address1='123 Test St',
            default_street_address2='Apt 456',
            default_county='Test County',
        )
        cls.order = Order.objects.create(
            order_number='12345678',
            user=cls.user,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test St',
            street_address2='Apt 456',
            county='Test County',
        )

    def test_profile_view_status_code(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_order_history_view_status_code(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('order_history', args=[self.order.order_number]))
        self.assertEqual(response.status_code, 200)
