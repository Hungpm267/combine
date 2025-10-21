from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category


class CategoryTestAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="username", password="123")
        self.client.force_authenticate(user = self.user)
        self.client.login(username = "username", password = "123")
        
        self.category = Category.objects.create(name, parent, image)
        
    def test_api_get_category(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_api_post_category(self):
        response = self.client.post(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_api_detail_category(self):
        response = self.client.get(reverse('categories'), pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_api_put_category(self):
        response = self.client.get(reverse('categories'), pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_patch_category(self):
        response = self.client.get(reverse('categories'), pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_api_delete_category(self):
        response = self.client.get(reverse('categories'), pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_count_number_of_product_each_categoty(self):
        response = self.client.get(reverse('categories'), pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    