"""
Custom filter classes for the API application.

This module defines custom filter sets for Book and Author models to provide
advanced filtering capabilities using django-filter.
"""

import django_filters
from django_filters import rest_framework as filters
from .models import Book, Author

class BookFilter(filters.FilterSet):
    """
    Custom filter set for Book model with advanced filtering options.
    
    Provides filtering capabilities on various book attributes including
    range filters for publication year and exact match filters for other fields.
    """
    
    publication_year_min = filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte',
        help_text="Filter books published in or after this year"
    )
    publication_year_max = filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte',
        help_text="Filter books published in or before this year"
    )
    
    title = filters.CharFilter(
        lookup_expr='icontains',
        help_text="Filter books by title (case-insensitive contains)"
    )
    author_name = filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text="Filter books by author name (case-insensitive contains)"
    )
    
    publication_year = filters.NumberFilter(
        help_text="Filter books by exact publication year"
    )
    author = filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        help_text="Filter books by specific author"
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
            'author': ['exact'],
        }
    
    @property
    def qs(self):
        """
        Custom queryset method to add additional filtering logic.
        
        Returns:
            QuerySet: Filtered book queryset
        """
        queryset = super().qs
        
        
        return queryset

class AuthorFilter(filters.FilterSet):
    """
    Custom filter set for Author model.
    
    Provides filtering capabilities for author attributes.
    """
    
    name = filters.CharFilter(
        lookup_expr='icontains',
        help_text="Filter authors by name (case-insensitive contains)"
    )
    
    min_books = filters.NumberFilter(
        method='filter_min_books',
        help_text="Filter authors with at least this many books"
    )
    max_books = filters.NumberFilter(
        method='filter_max_books',
        help_text="Filter authors with at most this many books"
    )
    
    class Meta:
        model = Author
        fields = ['name']
    
    def filter_min_books(self, queryset, name, value):
        """
        Custom method to filter authors by minimum book count.
        
        Args:
            queryset: The author queryset
            name: The field name
            value: The minimum book count value
            
        Returns:
            QuerySet: Filtered author queryset
        """
        return queryset.annotate(book_count=models.Count('books')).filter(book_count__gte=value)
    
    def filter_max_books(self, queryset, name, value):
        """
        Custom method to filter authors by maximum book count.
        
        Args:
            queryset: The author queryset
            name: The field name
            value: The maximum book count value
            
        Returns:
            QuerySet: Filtered author queryset
        """
        return queryset.annotate(book_count=models.Count('books')).filter(book_count__lte=value)