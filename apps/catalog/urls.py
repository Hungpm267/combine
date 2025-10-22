from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet)

product_router = routers.NestedDefaultRouter(router, r'products', lookup = 'product')
product_router.register(r'comments', CommentViewSet, basename='product-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls))
]