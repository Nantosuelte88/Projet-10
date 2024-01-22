from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('SoftDeskAPI.urls')),
    path('', include('authentication.urls')),
]
