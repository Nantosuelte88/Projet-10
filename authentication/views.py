from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from authentication.models import User
from authentication.serializers import UserSerializer, UserListSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsUserSelf

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from authentication.forms import UserRegistrationForm


class UserRegistrationView(generics.CreateAPIView):
    # Vue basée sur la classe generics.CreateAPIView pour l'enregistrement des utilisateurs.
    # Utilise le sérialiseur UserSerializer et le formulaire UserRegistrationForm.

    serializer_class = UserSerializer
    form_class = UserRegistrationForm

    def perform_create(self, serializer):
        # Méthode qui effectue la création de l'utilisateur.
        form = self.form_class(self.request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            serializer.save()


class UserListView(generics.ListCreateAPIView):
    # Vue basée sur la classe generics.ListCreateAPIView pour afficher et créer des utilisateurs.
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    form_class = UserRegistrationForm

    def create(self, request, *args, **kwargs):
        # Méthode qui crée un nouvel utilisateur.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data['password'])  # Hacher le mot de passe
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Vue basée sur la classe generics.RetrieveUpdateDestroyAPIView pour afficher,
    # mettre à jour et supprimer un utilisateur spécifique
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserSelf]


class UserLoginApiView(ObtainAuthToken):
    # Vue basée sur la classe ObtainAuthToken pour l'authentification d'un utilisateur.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

