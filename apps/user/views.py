from django.shortcuts import render
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer

# Create your views here.


class UserViewSet(mixins.CreateModelMixin, 
                  viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()
    
    @action(detail =False, methods = ['get'], url_path='me')
    def get_me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

