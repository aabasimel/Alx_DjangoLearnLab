"""
API views for the Author and Book models.
"""

from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
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


class BookListView(generics.ListAPIView):
    """List view for retrieving all books with filtering and search capabilities.
    This view provides read-only access to all Book instances and includes
    filtering, searching and ordering functionalities.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'author__name']
    search_fields = ['title',           
        'title__icontains', 
        'author__name',    
        'author__name__icontains', ]
    ordering_fields = ['title',
        'publication_year',
        'created_at',
        'updated_at',
        'author__name', ]
    permission_classes = [permissions.AllowAny]

class BookDetailView(generics.RetrieveAPIView):
    """Detail view for retrieving a single book instance.
    This view provides read-only access to a single Book instance identified
    by its primary key.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    """Create view for adding a new book instance.
    This view allows authenticated users to create new Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book = serializer.save()



class BookUpdateView(generics.UpdateAPIView):
    """Update view for modifying an existing book instance.
    This view allows authenticated users to update existing Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    def perform_update(self, serializer):
        original = self.get_object()
        update_book = serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        instance.delete()
class AuthorListView(generics.ListAPIView):
    """List view for retrieving all authors.
    This view provides read-only access to all Author instances.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    serach_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    """Detail view for retrieving a single author instance.
    This view provides read-only access to a single Author instance identified
    by its primary key.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class AuthorCreateView(generics.CreateAPIView):
    """Create view for adding a new author instance.
    This view allows authenticated users to create new Author instances.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorUpdateView(generics.UpdateAPIView):
    """Update view for modifying an existing author instance.
    This view allows authenticated users to update existing Author instances.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

class AuthorDeleteView(generics.DestroyAPIView):
    """Delete view for removing an existing author instance.
    This view allows authenticated users to delete existing Author instances.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

class BookBulkOperationsView(generics.GenericAPIView):
    """View for performing bulk operations on Book instances.
    This view allows authenticated users to create, update, or delete
    multiple Book instances in a single request.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.all()
    def post(self, request, *args, **kwargs):
       
        return Response(
            {"message": "Bulk operations endpoint - implement specific logic as needed"},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    