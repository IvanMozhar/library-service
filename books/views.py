from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS

from books.models import Book
from books.serializers import BookSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser | ReadOnly]
