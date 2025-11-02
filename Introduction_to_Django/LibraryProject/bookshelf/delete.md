
**File: `delete.md`**
```markdown
# Delete Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Expected output
# (1, {'bookshelf.Book': 1}) - indicates one object was deleted