from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from authentication.models import User
from authentication.serializers import UserSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from authentication.forms import UserRegistrationForm


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    form_class = UserRegistrationForm

    def perform_create(self, serializer):
        form = self.form_class(self.request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            serializer.save()


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    form_class = UserRegistrationForm

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data['password'])  # Hacher le mot de passe
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

