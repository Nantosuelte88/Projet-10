from rest_framework import generics
from authentication.models import User
from authentication.serializers import UserSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
