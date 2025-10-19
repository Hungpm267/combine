from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Category, Product,Comment
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=False, url_path='stats')
    def dem_so_product_tung_category(self, request):
        """
        đếm số sản phẩm trên từng thể loại
        """
        truyvan = Category.objects.annotate(product_count=Count('products')).values('name', 'product_count').all()
        return Response(truyvan)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count+=1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='stats')
    def dem_so_comment_tung_product(self, request):
        truyvan = Product.objects.annotate(comment_count=Count('comments')).values('comment_count', 'name').all()
        return Response(truyvan)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]