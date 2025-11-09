import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from .models import Author, Book, Library, Librarian

def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name: {author_name}")

def books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name} librarty: ")

        for book in books:
            print(f"- {book.title} by {book.author.name}")

    except Library.DoesNotExist:
        print(f"Library {library_name} not found")
        return []

def librarian_for_library(library_name):
    """
    Retrieve the librarian for a library
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Using OneToOne relationship
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")
        return None

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