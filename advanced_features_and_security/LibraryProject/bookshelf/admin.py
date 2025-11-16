from django.contrib import admin
from .models import Author, Book, Library, Librarian,UserProfile,CustomUser
from django.contrib.auth.admin import UserAdmin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['books']

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ['name', 'library']

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth', 'profile_photo']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups','date_of_birth']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'date_of_birth',
                'profile_photo',
                'is_staff',
                'is_active'
            )}
        ),)
    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
   
