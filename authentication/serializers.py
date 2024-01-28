from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = '__all__'
