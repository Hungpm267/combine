from django.db import models
from mptt.models import MPTTModel, TreeForeignKey 
from django.contrib.auth.models import User
# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=250, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name = 'children', null = True, blank=True)
    image = models.ImageField(upload_to='imageOfCategory', blank=True, null=True)

    class MPTTMeta:
        # Sắp xếp các category cùng cấp theo tên
        order_insertion_by = ['name']

    def __str__(self):
        return f"category tên: ({self.name}) "


class Product(models.Model):
    name = models.CharField(max_length=250)
    thumbnail = models.ImageField(upload_to='thumbnailOfProduct', blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='products')
    description = models.TextField()
    view_count = models.PositiveIntegerField(default= 0)
    comment = models.TextField(blank = True, null=True)
    editing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='editingUser', null=True, blank=True)
    editing_ends_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"product tên: ({self.name})"
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to="imagesOfProduct")

    def __str__(self):
        return f"đây là images của {self.product.name}"

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    def __str__(self):
        return f"comment của ({self.user.username}) trên sản phẩm ({self.product.name})"
                             