from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Item


class ItemViewSetTests(APITestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()

        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Create a sample item
        self.item = Item.objects.create(name="Test Item", description="A test item description")

    def authenticate(self):
        # Authenticate using the JWT token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_get_items_without_authentication(self):
        """
        Ensure that unauthenticated requests are forbidden.
        """
        url = '/api/items/'  # Updated to match your actual URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_items_with_authentication(self):
        """
        Ensure that authenticated requests can retrieve items.
        """
        self.authenticate()
        url = '/api/items/'  # Updated to match your actual URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return one item
        self.assertEqual(response.data[0]['name'], self.item.name)

    def test_create_item(self):
        """
        Ensure that authenticated users can create new items.
        """
        self.authenticate()
        url = '/api/items/'  # Updated to match your actual URL
        data = {
            'name': 'New Test Item',
            'description': 'A description for the new item'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(Item.objects.last().name, 'New Test Item')

    def test_update_item(self):
        """
        Ensure that authenticated users can update existing items.
        """
        self.authenticate()
        url = f'/api/items/{self.item.pk}/'  # Updated to match your actual URL
        data = {
            'name': 'Updated Item',
            'description': 'Updated description'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()  # Reload the item from the database
        self.assertEqual(self.item.name, 'Updated Item')
        self.assertEqual(self.item.description, 'Updated description')

    def test_delete_item(self):
        """
        Ensure that authenticated users can delete an item.
        """
        self.authenticate()
        url = f'/api/items/{self.item.pk}/'  # Updated to match your actual URL
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
