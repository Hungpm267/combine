from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, F
from django.utils import timezone
from django.db import transaction
from .models import Category, Product,Comment, UserVoucher
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer





# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    """
    dùng để crud, đếm số sp trên từng category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=False, url_path='stats')
    def count_number_of_product_each_categoty(self):
        """
        đếm số sản phẩm trên từng thể loại
        """
        myquery = Category.objects.annotate(product_count=Count('products')).values(
            'name', 
            'product_count').all()
        return Response(myquery)


class ProductViewSet(viewsets.ModelViewSet):
    """
    doc của productviewset
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        """override lại retrieve của modelviewset"""
        instance = self.get_object()
        instance.view_count+=1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stats')
    def count_number_of_comment_per_product(self):
        """
        đếm số comment của từng product
        """
        myquery = Product.objects.annotate(comment_count=Count('comments')).values('comment_count', 'name').all()
        return Response(myquery)
    
    @action(detail=True, methods=['get'], url_path='editable')
    def check_editable(self, request, pk =None):
        """kiểm tra xem request.user có quyền edit hay không, nếu có quyền thì user vào luồng edit luôn"""
        try:
            product = self.get_object()
        except Product.DoesNotExist:
            return Response({'error': 'ko tồn tại product'}, status=status.HTTP_404_NOT_FOUND)
        
        is_expired = False
        if product.editing_ends_at is not None:
            is_expired = True if timezone.now() > product.editing_ends_at else False

        if (product.editing_user is None or product.editing_user == request.user or is_expired is True):
            product.editing_user = request.user
            product.editing_ends_at = timezone.now() + timedelta(minutes = 5)
            product.save()
            return Response({'notify': "bạn có thể edit sản phẩm này"}, status=status.HTTP_200_OK)
        else:
            return Response({'notify': 'bạn ko thể edit sản phẩm này vì có người khác đang edit'}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail = True, methods=['post'], url_path='release')
    def release_edit(self, request):
        """hàm bỏ quyeenf edit cho usser khac edit"""
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
            return Response({'notify': 'release khóa thất bại'}, status=status.HTTP_403_FORBIDDEN)
            
    @action(detail=True, methods = ['post'], url_path='maintain')
    def maintain_edit(self, request):
        """hàm tăng biến editing_ends_at them 5 phút"""
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
        """hàm nhận cho user nhận voucher"""
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk= pk )
            has_voucher = UserVoucher.objects.filter(user = request.user, product = product).exists()
            if not product.voucher_enable:
                return Response({'notify': 'san pham nay ko co voucher'}, status=status.HTTP_204_NO_CONTENT)
            if product.voucher_quantity <= 0:
                return Response({'notify': 'da het voucher roi'}, status=status.HTTP_404_NOT_FOUND)
            if has_voucher:
                return Response({'notify': 'ban da co voucher nay roi'}, status=status.HTTP_403_FORBIDDEN)
                     
            # product.voucher_quantity -= 1
            # product.save(update_fields=['voucher_quantity'])
            Product.objects.filter(pk=pk).update(voucher_quantity = F('voucher_quantity') - 1)
            voucherid = f"VOUCHER-NO-{request.user.id}"
            voucher = UserVoucher.objects.create(voucher_code = voucherid, user = request.user, product = product)    
            return Response({'notify': f'nhan voucher thanh cong với mã là {voucher}'}, status=status.HTTP_200_OK)
class CommentViewSet(viewsets.ModelViewSet):
    """crud cho comment """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]