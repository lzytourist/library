from django.urls import path

from .views import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView, \
    BorrowAPIView, ReturnAPIView

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='books'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book'),
    path('borrow/', BorrowAPIView.as_view(), name='borrow'),
    path('return/', ReturnAPIView.as_view(), name='return'),
]