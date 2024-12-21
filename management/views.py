import datetime

from django.conf import settings
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Fine, Borrow
from .permissions import IsAdmin, IsMember
from .serializers import BookSerializer, BorrowSerializer, ReturnSerializer, FineSerializer


class BookListCreateAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return super().get_permissions()


class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class BorrowAPIView(APIView):
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ReturnAPIView(APIView):
    serializer_class = ReturnSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        borrow = serializer.validated_data['borrow']

        # Update available copies
        book = borrow.book
        book.available_copies += 1
        book.save()

        # Update borrowed status
        borrow.status = Borrow.Status.RETURNED
        borrow.save()

        if (datetime.date.today() - borrow.return_date).days > 0:
            # Fine calculation in case of overdue
            fine_amount = settings.OVERDUE_FINE * (datetime.date.today() - borrow.return_date).days
            fine = Fine.objects.create(
                member=request.user,
                borrow=borrow,
                amount=fine_amount,
                status=Fine.Status.UNPAID
            )

            return Response(
                data={
                    'message': 'Book has been returned. Please pay the overdue fine.',
                    'fine': FineSerializer(fine).data,
                }
            )

        return Response(data={
            'message': 'Book has been returned.',
        })
