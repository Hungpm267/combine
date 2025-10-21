

from .models import Category, Product, ProductImage, Comment
from rest_framework import serializers
from rest_framework.response import Response

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'image' ]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image' ]

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Comment
        fields = ['user', 'product', 'content']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many = True, read_only = True, source = "product_image")
    category = CategorySerializer(many = True)
    comment = CommentSerializer(many =True, source = 'comments')
    class Meta:
        model = Product
        fields = ['id', 'name', 'thumbnail', 'category', 'description', 'images', 'comment', 'view_count', 
                  'voucher_enable', 'voucher_quantity']



    