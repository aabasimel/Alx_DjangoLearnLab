# Updating a book title

from bookshelf.models import Book

book = Book.objects.get(title="1984")

book.title = "Nineteen Eighty-Four"
book.save()
book

# <Book: Title: 'Nineteen Eighty-Four', Author: 'George Orwell', Publication Year: 1949>