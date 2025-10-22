from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Product


class CategoryTestAPI(APITestCase):
    """kiểm tra các api với category hoạt động đúng chưa"""
    def setUp(self):
        self.user = User.objects.create_user(username="username", password="123")
        self.client.force_authenticate(user = self.user)
        
        self.category_dad = Category.objects.create(name = "đồ dùng điện tử")
        self.category_son = Category.objects.create(name= "laptop", parent = self.category_dad)

        self.product = Product.objects.create(name="lenovo thinkpad", category=self.category_son, description="25 triệu")
        self.product = Product.objects.create(name="lenovo IBM", category=self.category_son, description="30 triệu")

        self.reverse
        # ============================================================================================
        
    def test_get_category_list_success(self):
        """  test api lấy list các category  """
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # ============================================================================================
        
    def test_api_get_category_detail_success(self):
        """ test api lấy detail category bất kì """
        response = self.client.get(reverse('category-detail', kwargs={"pk": self.category_dad.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category_dad.name)

        
        # ============================================================================================
        
    def test_api_post_category_success(self):
        """ test api tạo category mới có thành công hay không """
        data = {
            'name': "oven",
            'parent': self.category_dad.pk
        }
        response = self.client.post(reverse('category-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "oven")
        self.assertEqual(Category.objects.count(), 3)
        # ============================================================================================

    def test_api_post_category_failed(self):
        """ test api tạo category mới thất bại """
        data = {
            # 'name': "oven", => data is missed
            'parent': self.category_dad.pk
        }
        response = self.client.post(reverse('category-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['name'], "oven")
        self.assertEqual(Category.objects.count(), 2)
        
        # ================================================DOING IT============================================
        
    def test_api_put_category(self):
        """ test xem chức năng put category với id chỉ định có hoạt động thành công ko """
        data = {
            'name': "đồ dùng nhựa",
        }
        response = self.client.put(reverse('category-detail', kwargs={"pk": self.category_dad.pk}), data, format='json')
        result = self.category_dad.refresh_from_db()
        self.assertEqual(result.data['name'], "đồ dùng nhựa")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        
        # ============================================================================================
        
    def test_api_detail_category_failed(self):
        """ tét xem chức năng detail category hoạt động false """
        data = {
            'name': "đồ dùng nhựa",
            'parent': "building",
            "image": "null"
        }
        response1 = self.client.post(reverse('categories'), data, format='json')
        
        response = self.client.get(reverse('categories'), pk = response1.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # ============================================================================================
        
    def test_api_put_category_success(self):
        """ test xem put category có chạy thành công ko """
        data = {
            'name': "office",
            'parent': "building"
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
    