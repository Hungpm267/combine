from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category


class CategoryTestAPI(APITestCase):
    """kiểm tra các api với category hoạt động đúng chưa"""
    def setUp(self):
        self.user = User.objects.create_user(username="username", password="123")
        self.client.force_authenticate(user = self.user)
        self.client.login(username = "username", password = "123")
        self.category = Category.objects.create(name, parent, image)
        
        # ============================================================================================
        
    def test_api_get_category(self):
        """  test api lấy list các category  """
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # ============================================================================================
        
    def test_api_get_category_failed(self):
        """ test api lấy list các category thất bại """
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # ============================================================================================
        
    def test_api_post_category(self):
        """ test api tạo category mới có thành công hay không """
        data = {
            'name': "office",
            'parent': "building",
            "image": "null"
        }
        response = self.client.post(reverse('categories'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.get().name, 'office')
        # ============================================================================================

    def test_api_post_category_failed(self):
        """ test api tạo category mới thất bại """
        data = {
            'name': "office",
            'parent': "building",
            "image": "null"
        }
        response = self.client.post(reverse('categories'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.get().name, 'office')
        
        # ============================================================================================
        
    def test_api_detail_category(self):
        """ test xem chức năng xem detail category với id chỉ định có hoạt động thành công ko """
        data = {
            'name': "office",
            'parent': "building",
            "image": "null"
        }
        response1 = self.client.post(reverse('categories'), data, format='json')
        
        response = self.client.get(reverse('categories'), pk = response1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # ============================================================================================
        
    def test_api_detail_category_failed(self):
        """ tét xem chức năng detail category hoạt động false """
        data = {
            'name': "office",
            'parent': "building",
            "image": "null"
        }
        response1 = self.client.post(reverse('categories'), data, format='json')
        
        response = self.client.get(reverse('categories'), pk = response1.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # ============================================================================================
        
    def test_api_put_category(self):
        """ test xem put category có chạy thành công ko """
        data = {
            'name': "office",
            'parent': "building",
            "image": "null"
        }
        response1 = self.client.post(reverse('categories'), data, format='json')
        
        data2 = {
            'name': "office mai son",
            'parent': "building",
            "image": "null"
        }
        response2 = self.client.put(reverse('categories'), data, format='json')
        
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        
        # ============================================================================================
        
    def test_api_put_category_failed(self):
        """ tét api cập nhật category thất bại """
        
        data = {
            'name': "office",
            'parent': "building",
            "image": "null"
        }
        response1 = self.client.post(reverse('categories'), data, format='json')
        
        data2 = {
            'name': "office mai son",
            'parent': "building",
            "image": "null"
        }
        response2 = self.client.put(reverse('categories'), data, format='json')
        
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
    
        # ============================================================================================
        
    def test_api_delete_category(self):
        """ test xóa category thành công """
        data = {
            'name': "office",
            'parent': "building",
            "image": "null"
        }
        response1 = self.client.post(reverse('categories'), data, format='json')
        response = self.client.delete(reverse('categories'), pk = response1.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # ============================================================================================
    
    def test_api_count_number_of_product_each_categoty(self):
        response = self.client.get(reverse('categories'), pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    