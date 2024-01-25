from django.urls import path

from authentication.views import UserDetailView, UserListView, UserLoginApiView


urlpatterns = [
    path('login/', UserLoginApiView.as_view()),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
]
