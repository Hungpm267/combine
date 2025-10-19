from django.contrib import admin
from .models import Category, Product, ProductImage, Comment
from mptt.admin import MPTTModelAdmin 
# Register your models here.

admin.site.register(Category, MPTTModelAdmin)
# admin.site.register(Product)
# Dùng TabularInline để thêm nhiều ảnh ngay trên trang Product
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2 # Số lượng form trống để upload ảnh mới

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ('name')
    # list_filter = ('categories')
    # search_fields = ('name', 'description')
    filter_horizontal = ('category',) # Giao diện dễ chọn nhiều category
    inlines = [ProductImageInline]


admin.site.register(Comment)