
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Book URLs
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('books/<int:pk>/operations/', views.book_operations, name='book_operations'),
    
    # Author URLs
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author_create'),
    
    # Library URLs
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    path('libraries/<int:pk>/manage-books/', views.library_manage_books, name='library_manage_books'),
    
    # Dashboard and API URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/books/', views.api_books, name='api_books'),
    
    # Home page
    path('', views.dashboard, name='home'),
]