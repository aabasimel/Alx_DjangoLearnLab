from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,DeleteView,UpdateView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .models import Book, Author, Library, Librarian,UserProfile
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.decorators import permission_required
from .forms import BookForm, AuthorForm, LibraryForm,UserProfile
from django.urls import reverse
from django.http import JsonResponse
from .forms import ExampleForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def form_example(request):
    """
    Simple form example view
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Form submitted successfully!')
            return redirect('bookshelf:form_example_success')
    else:
        form = ContactForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

def form_example_success(request):
    """
    Success page after form submission
    """
    return render(request, 'bookshelf/form_example_success.html')
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('bookshelf.can_view_book_list'):
            messages.error(request, 'You do not have permission to view this page.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
class BookDetailView(LoginRequiredMixin, DetailView, PermissionRequiredMixin):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'
    redirect_field_name = 'redirect_to'
    permission_required = 'bookshelf.can_view_book_detail'
    raise_exception = True

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'book_create.html', {'form': form})

class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_update.html'
    context_object_name = 'book'
    permission_required = 'bookshelf.can_edit_book'
    raise_exception = True

    def get_success_url(self):
        messages.success(self.request, f'Book "{self.object.title}" has been updated successfully!')
        return reverse('book_detail', kwargs={'pk': self.object.pk})

class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'book_delete.html'
    context_object_name = 'book'
    permission_required = 'bookshelf.can_delete_book'
    raise_exception = True

    def get_success_url(self):
        messages.success(self.request, f'Book "{self.object.title}" has been deleted successfully!')
        return reverse('book_list')

    
class AuthorListView(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'author_list.html'
    context_object_name = 'authors'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
      
    def get_queryset(self):
        queryset = Author.objects.all()
        return queryset
class AuthorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author_create.html'
    permission_required = 'bookshelf.can_create_author'
    raise_exception = True
    
    def form_valid(self, form):
        return super().form_valid(form)
class LibraryListView(LoginRequiredMixin, ListView):
    model = Library
    template_name = 'library_list.html'
    context_object_name = 'libraries'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def get_queryset(self):
        queryset = Library.objects.all()
        return queryset

def library_manage_books(request, pk):
    library = get_object_or_404(Library, pk=pk)

    if request.method == 'POST':
        book_ids = request.POST.getlist('books')
        books = Book.objects.filter(pk__in=book_ids)
        library.books.set(books)
        return redirect('library_detail', pk=pk)

    available_books = Book.objects.filter(is_available = True)
    return render(request, 'library_manage_books.html', {'library': library, 'available_books': available_books})

@login_required
def dashboard(request):
    context = {}
    
    if request.user.has_perm('users.can_view_book'):
        context['recent_books'] = Book.objects.all()[:5]
        context['total_books'] = Book.objects.count()
    
    if request.user.has_perm('users.can_create_book'):
        context['can_create_book'] = True
    
    if request.user.has_perm('users.can_view_author'):
        context['recent_authors'] = Author.objects.all()[:5]
        context['total_authors'] = Author.objects.count()
    
    if request.user.has_perm('users.can_view_library'):
        context['libraries'] = Library.objects.all()
        context['total_libraries'] = Library.objects.count()
    
    user_profile = request.user.profile
    context['user_role'] = user_profile.role
    context['has_library_access'] = user_profile.has_library_access()
    
    return render(request, 'dashboard.html', context)

@login_required
def api_books(request):
    if not request.user.has_perm('users.can_view_book'):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    books = Book.objects.values('id', 'title', 'author__name', 'is_available')
    return JsonResponse(list(books), safe=False)

def check_model_permissions(user, model, actions=['view']):
    app_label = model._meta.app_label
    model_name = model._meta.model_name
    
    permissions = {}
    for action in actions:
        perm_codename = f'can_{action}_{model_name}'
        permissions[action] = user.has_perm(f'{app_label}.{perm_codename}')
    
    return permissions

@login_required
def book_operations(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    book_permissions = check_model_permissions(
        request.user, 
        Book, 
        ['view', 'create', 'edit', 'delete']
    )
    
    context = {
        'book': book,
        'permissions': book_permissions,
    }
    
    return render(request, 'books/book_operations.html', context)


