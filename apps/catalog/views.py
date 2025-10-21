from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Category, Product,Comment, UserVoucher
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.db import transaction

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
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    
    @action(detail=True, methods=['get'], url_path='editable')
    def check_editable(self, request, pk =None):
        try:
            product = self.get_object()
        except Product.DoesNotExist:
            return Response({'error': 'ko tồn tại product'}, status=status.HTTP_404_NOT_FOUND)
        
        is_expired = False
        if product.editing_ends_at is not None:
            is_expired = True if timezone.now() > product.editing_ends_at else False
            
        
        if (product.editing_user is None or product.editing_user == request.user or is_expired ==True):
            product.editing_user = request.user
            product.editing_ends_at = timezone.now() + timedelta(minutes = 5)
            product.save()
            return Response({'notify': "bạn có thể edit sản phẩm này"}, status=status.HTTP_200_OK)
        else:
            return Response({'notify': 'bạn ko thể edit sản phẩm này vì có người khác đang edit'}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail = True, methods=['post'], url_path='release')
    def release_edit(self, request, pk = None):
        try:
            product = self.get_object()
        except Product.DoesNotExist:
            return Response({'error': 'ko tồn tại product'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == product.editing_user:
            product.editing_user = None
            product.editing_ends_at = None
            product.save()
            return Response({'notify': 'release khóa thành công'}, status=status.HTTP_200_OK)
        else:
            return Respone({'notify': 'release khóa thất bại'}, status=status.HTTP_403_FORBIDDEN)
            
    @action(detail=True, methods = ['post'], url_path='maintain')
    def maintain_edit(self, request, pk):
        try:
            product = self.get_object()
        except Product.DoesNotExist:
            return Response({'error': 'ko tồn tại product'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == product.editing_user:
            product.editing_ends_at= timezone.now() + timedelta(minutes = 5)
            product.save()
            return Response({'notify': 'gia han thanh cong'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'notify': 'bạn ko thể gia hạn khóa này'}, status=status.HTTP_403_FORBIDDEN)
        
    @action(detail=True, methods=['post'], url_path='claim_voucher')
    def claim_voucher(self, request, pk=None):
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk= pk )
            has_voucher = UserVoucher.objects.filter(user = request.user, product = product).exists()
            if has_voucher:
                return Response({'notify': 'ban da co voucher nay roi'}, status=status.HTTP_403_FORBIDDEN)
            if not product.voucher_enable:
                return Response({'notify': 'san pham nay ko co voucher'}, status=status.HTTP_204_NO_CONTENT)
            if product.voucher_quantity <= 0:
                return Response({'notify': 'da het voucher roi'}, status=status.HTTP_404_NOT_FOUND)
            
            product.voucher_quantity -= 1
            product.save(update_fields=['voucher_quantity'])
            voucherid = f"VOUCHER-NO-{request.user.id}"
            voucher = UserVoucher.objects.create(voucher_code = voucherid, user = request.user, product = product)
            
            return Response({'notify': 'nhan voucher thanh cong'}, status=status.HTTP_200_OK)

                
                
            
    


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]