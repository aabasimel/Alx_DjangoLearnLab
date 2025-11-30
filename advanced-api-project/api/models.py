from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the author's name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    """
    Book model representing a published book.
    
    Attributes:
        title (CharField): The title of the book (max 200 characters).
        publication_year (IntegerField): The year the book was published.
        author (ForeignKey): Reference to the Author who wrote the book.
        created_at (DateTimeField): Timestamp when the book record was created.
        updated_at (DateTimeField): Timestamp when the book record was last updated.
    """
    title = models.CharField(max_length=200,help_text="Enter the book title")
    publication_year = models.IntegerField(
        validators=[MinValueValidator(1450), MaxValueValidator(timezone.now().year)],
        help_text="Enter the year the book was published"
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author.name} "