from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User 
from .models import Product, Category

class ProductViewTests(TestCase):
    def setUpTestData(cls):
        # Set up test data, including creating products and categories.
        cls.user = User.objects.create_superuser(
            username='admin',
            password='adminpassword'
        )
        cls.category = Category.objects.create(name='Test Category')
        cls.product = Product.objects.create(
            name='Test Product',
            description='A test product',
            price=10.00,
            category=cls.category
        )

    def test_all_products_view_status_code(self):
        response = self.client.get(reverse('all_products'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_status_code(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)


