
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product

class BagViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing authentication (if needed)
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create some test products
        cls.product1 = Product.objects.create(
            name='Product 1',
            price=10.99
        )

    def setUp(self):
        self.client = Client()

    def test_view_bag_view(self):
        # Log in the user if authentication is required
        self.client.login(username='testuser', password='testpassword')

        # Visit the bag page
        response = self.client.get(reverse('view_bag'))

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Add some products to the bag 
        session = self.client.session
        session['bag'] = {
            str(self.product1.id): {
                'quantity': 2,
                'colour': 'Red',  
            }
        }
        session.save()

        # Check if the products added to the bag are displayed
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Red') 

    def test_add_to_bag_view(self):
        # Log in the user if authentication is required
        self.client.login(username='testuser', password='testpassword')

        # Send a POST request to add a product to the bag
        response = self.client.post(
            reverse('add_to_bag', args=[self.product1.id]),
            {'quantity': 2}
        )

        # Check if the response is a redirect (successful or Not)
        self.assertEqual(response.status_code, 302)

        # Check if the product is now in the user's bag
        session = self.client.session
        self.assertIn(str(self.product1.id), session['bag'])
        self.assertEqual(session['bag'][str(self.product1.id)]['quantity'], 2)

    def test_adjust_bag_view(self):
        # Log in the user if authentication is required
        self.client.login(username='testuser', password='testpassword')

        # Add a product to the bag 
        session = self.client.session
        session['bag'] = {
            str(self.product1.id): {
                'quantity': 2,
                'colour': 'Red', 
            }
        }
        session.save()

        # Send a POST request to adjust the quantity of the product in the cart
        response = self.client.post(
            reverse('adjust_bag', args=[self.product1.id]),
            {'quantity': 3}
        )

        # Check if the response is a redirect (successful adjustment)
        self.assertEqual(response.status_code, 302)

        # Check if the product's quantity in the cart is updated
        session = self.client.session
        self.assertIn(str(self.product1.id), session['bag'])
        self.assertEqual(session['bag'][str(self.product1.id)]['quantity'], 3)

    def test_remove_from_bag_view(self):
        # Log in the user if authentication is required
        self.client.login(username='testuser', password='testpassword')

        # Add a product to the bag 
        session = self.client.session
        session['bag'] = {
            str(self.product1.id): {
                'quantity': 2,
                'colour': 'Red',  
            }
        }
        session.save()

        # Send a POST request to remove the product from the bag
        response = self.client.post(
            reverse('remove_from_bag', args=[self.product1.id])
        )

        # Check if the response is a success (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if the product is removed from the bag
        session = self.client.session
        self.assertNotIn(str(self.product1.id), session['bag'])
