


from django.urls import path, include

urlpatterns = [
    path('catalog/', include('apps.catalog.urls')),
    path('user/', include('apps.user.urls'))
]