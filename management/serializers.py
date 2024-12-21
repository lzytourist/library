import datetime

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from .models import User, Book, Borrow, Fine


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


class BorrowSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        member = self.context['request'].user
        if member.borrowed.filter(status=Borrow.Status.BORROWED).count() >= settings.BORROW_LIMIT:
            raise serializers.ValidationError("You have reached maximum borrow limit")

        book = attrs.get('book')
        if not book.is_available():
            raise serializers.ValidationError("Book is not available")

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data.get('book')
            book.available_copies = book.available_copies - 1
            book.save()

            validated_data['member'] = self.context['request'].user
            validated_data['return_date'] = datetime.date.today() + datetime.timedelta(days=settings.BORROW_DAYS_LIMIT)

            return super().create(validated_data)

    class Meta:
        model = Borrow
        fields = '__all__'
        extra_kwargs = {
            'member': {'read_only': True},
            'member_id': {'read_only': True},
            'status': {'read_only': True},
        }


class BorrowDetailSerializer(BorrowSerializer):
    book = BookSerializer(read_only=True)
    is_overdue = serializers.SerializerMethodField()

    @staticmethod
    def get_is_overdue(obj):
        return (datetime.date.today() - obj.return_date).days > 0


class ReturnSerializer(serializers.Serializer):
    borrow = serializers.PrimaryKeyRelatedField(queryset=Borrow.objects.all())

    def validate(self, attrs):
        borrow = attrs.get('borrow')
        if borrow.member_id != self.context['request'].user.id:
            raise serializers.ValidationError("Invalid borrow id")

        if borrow.status != Borrow.Status.BORROWED:
            raise serializers.ValidationError("Book has already been returned")

        return attrs


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = '__all__'
