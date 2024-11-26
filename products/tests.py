from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product
import uuid

class ProductAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        
        self.product = Product.objects.create(
            uuid=uuid.uuid4(),
            name='Test Product',
            description='A test product description',
            price=49.99,
            owner=self.user
        )
        
        self.product_list_url = '/api/products/'
        self.product_detail_url = f'/api/products/{self.product.uuid}/'
        
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'password123'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_product_list(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_product(self):
        data = {
            'name': 'New Product',
            'description': 'A new product description',
            'price': 29.99
        }
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Product')

    def test_get_product_detail(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product(self):
        data = {
            'name': 'Updated Product Name',
            'description': 'Updated description',
            'price': 59.99
        }
        response = self.client.put(self.product_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product Name')

    def test_delete_product(self):
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(uuid=self.product.uuid).exists())

    def test_unauthenticated_access(self):
        self.client.credentials()  # Remove authentication
        data = {
            'name': 'Unauthorized Product',
            'description': 'Should fail',
            'price': 19.99
        }
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
