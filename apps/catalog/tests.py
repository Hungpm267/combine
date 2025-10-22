from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from apps.catalog.models import Category, Product


class CategoryTestAPI(APITestCase):
    """kiểm tra các api với category hoạt động đúng chưa"""
    def setUp(self):
        self.user = User.objects.create_user(username="username", password="123")
        self.client.force_authenticate(user = self.user)
        
        self.category_dad = Category.objects.create(name = "đồ dùng điện tử")
        self.category_son = Category.objects.create(name= "laptop", parent = self.category_dad)

        self.product = Product.objects.create(name="lenovo thinkpad", description="25 triệu")
        self.product.category.add(self.category_son)
        self.product = Product.objects.create(name="lenovo IBM", description="30 triệu")
        self.product.category.add(self.category_son)

        # ============================================================================================
        
    def test_get_category_list_success(self):
        """  test api lấy list các category  """
        response = self.client.get(reverse('category-list'))
        
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
            'parent': self.category_dad.pk,
            "image": None
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
        self.assertEqual(Category.objects.count(), 2)
        
        # ============================================================================================
        
    def test_api_put_category(self):
        """ test xem chức năng put category với id chỉ định có hoạt động thành công ko """
        data = {
            'name': "đồ dùng điện tử năm 1990",
            'parent': None,
            'image': None
        }
        response = self.client.put(reverse('category-detail', kwargs={"pk": self.category_dad.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category_dad.refresh_from_db()
        self.assertEqual(self.category_dad.name, "đồ dùng điện tử năm 1990")    
    
        # ========================================DOING IT====================================================
        
    def test_api_delete_category(self):
        """ test xóa category thành công """
        response = self.client.delete(reverse('category-detail', kwargs = {"pk": self.category_son.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)
        
        # ============================================================================================

    