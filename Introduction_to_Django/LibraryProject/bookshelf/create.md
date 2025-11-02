# Create a Book instance
`# Create Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Book object created successfully
# No explicit output, but object is created in database