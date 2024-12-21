from django.urls import path

from .views import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView, \
    BorrowAPIView, ReturnAPIView, BorrowListAPIView, BorrowRetrieveAPIView, \
    FineListAPIView, FineRetrieveAPIView

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='books'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book'),
    path('borrow/', BorrowAPIView.as_view(), name='borrow'),
    path('return/', ReturnAPIView.as_view(), name='return'),
    path('borrow-history/', BorrowListAPIView.as_view(), name='borrow-list'),
    path('borrow-details/<int:pk>/', BorrowRetrieveAPIView.as_view(), name='borrow-details'),
    path('fines/', FineListAPIView.as_view(), name='fines'),
    path('fines/<int:pk>/', FineRetrieveAPIView.as_view(), name='fine'),
]