from django.urls import path

from .views import BookListCreateAPIView, BookRetrieveUpdateDestoryAPIView

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='books'),
    path('books/<int:pk>/', BookRetrieveUpdateDestoryAPIView.as_view(), name='book'),
]