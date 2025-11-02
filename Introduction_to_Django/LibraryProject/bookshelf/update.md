# Update
```python
book.title = "Nineteen Eighty-Four"
book.save()
```

# Verify
```python
book_updated = Book.objects.get(id=book.id)
book_updated.title
```
# Output: 'Nineteen Eighty-Four'
