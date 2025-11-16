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


from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import html
import re
from .models import Book, Author, Library, User, UserProfile, Librarian

class ExampleForm(forms.ModelForm):
    """
    Base form with security enhancements.
    """
    def clean(self):
        cleaned_data = super().clean()
        
        # HTML escape all string fields to prevent XSS
        for field_name, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field_name] = html.escape(value)
        
        return cleaned_data

class BookForm(SecureModelForm):
    """
    Form for creating and updating books.
    """
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            # Prevent SQL injection in titles
            sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION']
            for keyword in sql_keywords:
                if keyword.lower() in title.lower():
                    raise ValidationError('Invalid characters in title.')
            
            # Limit title length
            if len(title) > 200:
                raise ValidationError('Title must be 200 characters or less.')
            
            # Remove any potentially dangerous characters
            title = re.sub(r'[<>]', '', title)
        
        return title

class AuthorForm(SecureModelForm):
    """
    Form for creating and updating authors.
    """
    class Meta:
        model = Author
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            })
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Prevent SQL injection in author names
            sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION']
            for keyword in sql_keywords:
                if keyword.lower() in name.lower():
                    raise ValidationError('Invalid characters in author name.')
            
            # Limit name length
            if len(name) > 100:
                raise ValidationError('Author name must be 100 characters or less.')
            
            # Remove any potentially dangerous characters
            name = re.sub(r'[<>]', '', name)
        
        return name

class LibraryForm(SecureModelForm):
    """
    Form for creating and updating libraries.
    """
    class Meta:
        model = Library
        fields = ['name', 'address', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter library name'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter library address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            })
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Validate phone number format
            if not re.match(r'^[\d\s\-\+\(\)]{10,15}$', phone_number):
                raise ValidationError('Please enter a valid phone number.')
        return phone_number

class LibrarianForm(SecureModelForm):
    """
    Form for creating and updating librarians.
    """
    class Meta:
        model = Librarian
        fields = ['user', 'library', 'employee_id']
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control'
            }),
            'library': forms.Select(attrs={
                'class': 'form-control'
            }),
            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter employee ID'
            })
        }

class UserProfileForm(SecureModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = UserProfile
        fields = ['role', 'bio', 'website']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            })
        }
    
    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website:
            # Basic URL validation
            if not website.startswith(('http://', 'https://')):
                raise ValidationError('Please enter a valid URL starting with http:// or https://')
            
            # Check for suspicious patterns in URL
            suspicious_patterns = [
                r'<script', r'javascript:', r'vbscript:',
                r'data:', r'%3Cscript'
            ]
            for pattern in suspicious_patterns:
                if re.search(pattern, website, re.IGNORECASE):
                    raise ValidationError('Invalid URL format.')
        
        return website

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users in the admin panel and registration.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating users in the admin panel.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }

class UserRegistrationForm(forms.ModelForm):
    """
    Form for user registration with security enhancements.
    """
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a strong password'
        }),
        help_text=_('Enter a strong password with at least 8 characters')
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        help_text=_('Enter the same password as above, for verification')
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

    def clean_password2(self):
        """
        Check that the two password entries match.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Check for SQL injection patterns
            sql_patterns = [r'--', r';', r'/*', r'*/', r'xp_', r'@@']
            for pattern in sql_patterns:
                if pattern in username.lower():
                    raise ValidationError('Invalid characters in username.')
            
            # Check for XSS patterns
            xss_patterns = [r'<script', r'</script>', r'onload', r'onerror', r'javascript:']
            for pattern in xss_patterns:
                if pattern in username.lower():
                    raise ValidationError('Invalid characters in username.')
        
        return username

    def clean_email(self):
        """Enhanced email validation with security checks"""
        email = self.cleaned_data.get('email')
        if email:
            # Basic email format validation
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValidationError('Please enter a valid email address.')
            
            # Check for suspicious patterns
            suspicious_patterns = [
                r'<script', r'javascript:', r'onload=', r'onerror=',
                r'vbscript:', r'expression', r'<iframe', r'<object'
            ]
            for pattern in suspicious_patterns:
                if re.search(pattern, email, re.IGNORECASE):
                    raise ValidationError('Invalid email format.')
        
        return email

    def save(self, commit=True):
        """
        Save the user with the provided password.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ExampleForm(forms.Form):
    """
    Example form demonstrating security best practices.
    This can be used as a template for new forms.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        }),
        help_text='Enter your full name'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message'
        })
    )
    
    agree_to_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='I agree to the terms and conditions'
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Sanitize input
            name = html.escape(name)
            
            # Check for SQL injection patterns
            sql_patterns = [r'--', r';', r'/*', r'*/', r'union', r'select']
            for pattern in sql_patterns:
                if re.search(pattern, name, re.IGNORECASE):
                    raise ValidationError('Invalid characters in name.')
        
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            # Basic XSS prevention
            dangerous_tags = ['script', 'iframe', 'object', 'embed', 'link']
            for tag in dangerous_tags:
                if f'<{tag}' in message.lower():
                    raise ValidationError('Message contains unsafe content.')
            
            # Limit message length
            if len(message) > 1000:
                raise ValidationError('Message must be 1000 characters or less.')
        
        return message

class SearchForm(forms.Form):
    """
    Secure search form with input validation.
    """
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books or authors...'
        })
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('books', 'Books'),
            ('authors', 'Authors'),
            ('both', 'Both')
        ],
        initial='both',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def clean_query(self):
        query = self.cleaned_data.get('query')
        if query:
            # Prevent SQL injection in search queries
            sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', 'OR 1=1']
            for keyword in sql_keywords:
                if keyword.lower() in query.lower():
                    raise ValidationError('Invalid search query.')
            
            # Remove potentially dangerous characters
            query = re.sub(r'[;\"\']', '', query)
            
            # Limit query length
            if len(query) > 100:
                raise ValidationError('Search query too long.')
        
        return query

class ContactForm(ExampleForm):
    """
    Contact form extending the secure ExampleForm.
    """
    subject = forms.ChoiceField(
        choices=[
            ('general', 'General Inquiry'),
            ('support', 'Technical Support'),
            ('feedback', 'Feedback'),
            ('other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    priority = forms.ChoiceField(
        choices=[
            ('low', 'Low'),
            ('normal', 'Normal'),
            ('high', 'High')
        ],
        initial='normal',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

class BulkUploadForm(forms.Form):
    """
    Form for bulk upload with file security validation.
    """
    file = forms.FileField(
        label='Select file to upload',
        help_text='Supported formats: CSV, JSON (Max 5MB)',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.json'
        })
    )
    
    file_type = forms.ChoiceField(
        choices=[
            ('csv', 'CSV'),
            ('json', 'JSON')
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (5MB limit)
            max_size = 5 * 1024 * 1024
            if file.size > max_size:
                raise ValidationError(f'File size must be under {max_size // 1024 // 1024}MB.')
            
            # Check file extension
            allowed_extensions = ['.csv', '.json']
            import os
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in allowed_extensions:
                raise ValidationError(f'File type {ext} is not allowed. Please upload CSV or JSON files.')
            
            # Check MIME type
            allowed_mime_types = ['text/csv', 'application/json', 'text/plain']
            if hasattr(file, 'content_type') and file.content_type not in allowed_mime_types:
                raise ValidationError('Invalid file type. Please upload CSV or JSON files.')
        
        return file