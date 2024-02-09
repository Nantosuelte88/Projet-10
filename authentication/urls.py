from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import UserDetailView, UserListView, UserRegistrationView


urlpatterns = [
    path('user-register/', UserRegistrationView.as_view(), name='user_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
]
