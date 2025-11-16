# Retrieving book instance

from bookshelf.models import Book

book = Book.objects.get(title="1984")
book

# <QuerySet [{'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}]>