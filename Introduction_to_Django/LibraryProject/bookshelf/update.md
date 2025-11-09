
**File: `update.md`**
```markdown
# Update Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Expected output
Updated title: Nineteen Eighty-Four