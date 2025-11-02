from django.contrib import admin
from .models import Book



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Enable searching by title and author
    search_fields = ('title', 'author')
    
    # Add filters for easier navigation
    list_filter = ('publication_year',)
# Register the Book model
admin.site.register(Book)