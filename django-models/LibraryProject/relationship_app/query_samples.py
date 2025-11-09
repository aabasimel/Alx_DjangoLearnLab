import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from .models import Author, Book, Library, Librarian

def books_by_author(author_name):
    books = Book.objects.filter(author__name=author_name)

    for book in books:
        print({book.title})

def books_in_library(library_name):
    library= Library.objects.get(name=library_name)
    print(f"books in {library.name}")
    for book in library.books.all():
        print(book.title)

def librarian_for_library(library_name):
    library=Library.objects.get(name=library_name)
    Librarian=library.librarian

if __name__ == "__main__":
    author, _ = Author.objects.get_or_create(name="J.K. Rowling")
    book1, _ = Book.objects.get_or_create(title="Harry Potter and the Sorcerer's Stone", author=author)
    book2, _ = Book.objects.get_or_create(title="Harry Potter and the Chamber of Secrets", author=author)
    library, _ = Library.objects.get_or_create(name="Central Library")
    library.books.add(book1, book2)
    librarian, _ = Librarian.objects.get_or_create(name="Emma Watson", library=library)

 
    books_by_author("J.K. Rowling")
    books_in_library("Central Library")
    librarian_for_library("Central Library")