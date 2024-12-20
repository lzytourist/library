from djoser.serializers import UserCreateSerializer

from .models import User


class UserSerializer(UserCreateSerializer):
    def create(self, validated_data):
        validated_data['role'] = User.Role.MEMBER
        return super().create(validated_data)
