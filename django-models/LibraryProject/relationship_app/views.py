from django.shortcuts import render, get_list_or_404,redirect
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Library, Author,Book, UserProfile

from django.views.generic.detail import DetailView

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test, login_required,permission_required
from .forms import BookForm

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'
def list_books(request):
    """
    Function-based view that lists all books in the database
    """
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})



@user_passes_test(is_admin)
@login_required
def admin_view(request):
    """
    Admin view - only accessible to users with Admin role
    """
    users = UserProfile.objects.all().select_related('user')
    return render(request, 'relationship_app/admin_view.html', {
        'users': users,
        'total_books': Book.objects.count(),
        'total_libraries': Library.objects.count(),
        'total_users': UserProfile.objects.count()
    })

@user_passes_test(is_librarian)
@login_required
def librarian_view(request):
    """
    Librarian view - only accessible to users with Librarian role
    """
    libraries = Library.objects.all().prefetch_related('books')
    return render(request, 'relationship_app/librarian_view.html', {
        'libraries': libraries,
        'total_books': Book.objects.count(),
        'available_books': Book.objects.filter(libraries__isnull=False).distinct().count()
    })
@user_passes_test(is_member)
@login_required
def member_view(request):
    """
    Member view - only accessible to users with Member role
    """
    books = Book.objects.all().select_related('author')
    libraries = Library.objects.all()
    return render(request, 'relationship_app/member_view.html', {
        'books': books,
        'libraries': libraries,
        'available_books_count': Book.objects.filter(libraries__isnull=False).distinct().count()
    })

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
    

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})
def LogoutView(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

@permission_required('relationship_app.can_add_book', raise_exception=True)
@login_required
def add_book(request):
    """
    View to add a new book - requires can_add_book permission
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been added successfully!')
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', raise_exception=True)
@login_required
def edit_book(request, book_id):
    """
    View to edit an existing book - requires can_change_book permission
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been updated successfully!')
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
@login_required
def delete_book(request, book_id):
    """
    View to delete a book - requires can_delete_book permission
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" has been deleted successfully!')
        return redirect('relationship_app:list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})
