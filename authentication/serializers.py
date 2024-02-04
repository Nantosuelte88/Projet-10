from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    # Serializer pour la classe User qui inclut les champs spécifiés dans la Meta classe.
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = ['id','is_active', 'username', 'email', 'date_of_birth',
                  'can_be_contacted', 'can_data_be_shared']


class UserListSerializer(serializers.ModelSerializer):
    # Serializer pour la liste des utilisateurs qui inclut les champs spécifiés dans la Meta classe.
    class Meta:
        model = User
        fields = ['id', 'username']
