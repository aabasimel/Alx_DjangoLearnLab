"""
API views for the Author and Book models.
"""

from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows authors to be viewed or created.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows detailed author operations.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows books to be viewed or created.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows detailed book operations.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer