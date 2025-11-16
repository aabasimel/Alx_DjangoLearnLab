from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import Book, Author, Library, User, UserProfile

class BookForm(forms.ModelForm):
    """
    Form for creating and updating books.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date', 'description', 'cover_image', 'is_available']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class AuthorForm(forms.ModelForm):
    """
    Form for creating and updating authors.
    """
    class Meta:
        model = Author
        fields = ['name', 'bio', 'date_of_birth', 'date_of_death']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class LibraryForm(forms.ModelForm):
    """
    Form for creating and updating libraries.
    """
    class Meta:
        model = Library
        fields = ['name', 'address', 'phone_number', 'email', 'opening_hours']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'opening_hours': forms.Textarea(attrs={'rows': 3}),
        }

class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = UserProfile
        fields = ['role', 'bio', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }