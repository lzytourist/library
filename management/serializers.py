from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from .models import User, Book


class UserSerializer(UserCreateSerializer):
    def create(self, validated_data):
        validated_data['role'] = User.Role.MEMBER
        return super().create(validated_data)


class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    @staticmethod
    def get_is_available(obj):
        return obj.is_available()
