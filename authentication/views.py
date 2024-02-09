from rest_framework import generics
from authentication.models import User
from authentication.serializers import UserSerializer, UserListSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsUserSelf

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


class UserListView(generics.ListAPIView):
    # Vue basée sur la classe generics.ListCreateAPIView pour afficher les utilisateurs.
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Vue basée sur la classe generics.RetrieveUpdateDestroyAPIView pour afficher,
    # mettre à jour et supprimer un utilisateur spécifique
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserSelf]
