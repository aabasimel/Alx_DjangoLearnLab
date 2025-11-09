from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Library, Author,Book
from django.views.generic.detail import DetailView
def list_books(request):
    """
    Function-based view that lists all books in the database
    """
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library'] = Library.objects.prefetch_related('books__author').get(pk=self.object.pk)
        return context