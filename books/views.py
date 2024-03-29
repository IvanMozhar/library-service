from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from books.models import Book
from books.permissions import ReadOnly
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser | ReadOnly]
