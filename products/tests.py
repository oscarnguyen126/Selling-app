from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Category
import uuid


class CategoryAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        
        # Create a sample category
        self.category = Category.objects.create(
            uuid=uuid.uuid4(),
            name="Electronics",
            description="All kinds of electronic products"
        )
        
        # Define URLs
        self.category_list_url = '/api/products/categories/'
        self.category_detail_url = f'/api/products/categories/{self.category.uuid}/'
        
        # Obtain token for authenticated requests
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'password123'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_category_list(self):
        response = self.client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]['name'], "Electronics")

    def test_create_category(self):
        data = {
            'name': 'Books',
            'description': 'Various kinds of books'
        }
        response = self.client.post(self.category_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Books')

    def test_get_category_detail(self):
        response = self.client.get(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Electronics')

    def test_update_category(self):
        data = {
            'name': 'Updated Electronics',
            'description': 'Updated description for electronics'
        }
        response = self.client.put(self.category_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Electronics')

    def test_delete_category(self):
        """Test deleting a category."""
        response = self.client.delete(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(uuid=self.category.uuid).exists())

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot create categories."""
        self.client.credentials()  # Remove authentication
        data = {
            'name': 'Unauthorized Category',
            'description': 'Should fail without authentication'
        }
        response = self.client.post(self.category_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
