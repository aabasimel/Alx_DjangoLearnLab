"""
Custom serializers for the API application.

This module defines serializers for the Author and Book models, including
nested relationships and custom validation logic.
"""

from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    Handles serialization/deserialization of Book instances and includes
    custom validation for the publication_year field.
    
    Attributes:
        publication_year: Custom validation ensures the year is not in the future.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_publication_year(self, value):
        """
        Validate that the publication year is not in the future.
        
        Args:
            value (int): The publication year to validate.
            
        Returns:
            int: The validated publication year.
            
        Raises:
            serializers.ValidationError: If the publication year is in the future.
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value
    
    def validate(self, data):
        """
        Object-level validation for Book instances.
        
        Args:
            data (dict): The data to validate.
            
        Returns:
            dict: The validated data.
        """
        
        return data

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer includes a nested representation of the author's books
    using the BookSerializer. The books field is read-only by default to
    handle the complexity of nested writes.
    
    Attributes:
        books (BookSerializer): Nested serializer for the author's books.
    """
    
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        """
        Customize the serialized representation.
        
        This method allows us to modify how the author data is presented,
        such as including additional computed fields or conditional data.
        
        Args:
            instance (Author): The Author instance being serialized.
            
        Returns:
            dict: The customized serialized representation.
        """
        representation = super().to_representation(instance)
        
        representation['book_count'] = instance.books.count()
        
        return representation

class AuthorDetailSerializer(AuthorSerializer):
    """
    Detailed Author serializer with additional book information.
    
    This extends the base AuthorSerializer to provide more detailed
    information about the author's books when needed.
    """
    
    class Meta(AuthorSerializer.Meta):
        fields = AuthorSerializer.Meta.fields + ['book_count']