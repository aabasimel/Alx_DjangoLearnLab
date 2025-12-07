# Authentication system for django_blog

This document describes the authentication features implemented in the `blog` app.

Features
- User registration (username + email + password)
- Login and logout using Django's built-in views
- Profile view to update first name, last name and email

Files added
- `blog/forms.py` — `RegistrationForm` (extends `UserCreationForm`) and `ProfileForm` (ModelForm for user profile updates).
- `blog/views.py` — `register` and `profile` views and an `index` view.
- `blog/urls.py` — routes for `login/`, `logout/`, `register/`, `profile/` and the app index.
- Templates under `blog/templates/registration/`:
  - `login.html` — used by Django's `LoginView`.
  - `register.html` — user registration form.
  - `profile.html` — profile editing form (requires login).
  - `logged_out.html` — displayed after logout.

How it works

1. Registration
   - Visit `/register/` and fill the form. The `RegistrationForm` requires an email address.
   - On success the user is created and automatically logged in.

2. Login / Logout
   - Visit `/login/` to log in. Django's `LoginView` is used and the template is at `registration/login.html`.
   - Visit `/logout/` to log out. `LogoutView` shows `registration/logged_out.html` and then redirects according to `LOGOUT_REDIRECT_URL`.

3. Profile
   - Authenticated users can visit `/profile/` to view and edit their first name, last name and email.

Security notes and testing
- All forms include CSRF tokens in templates.
- Passwords are stored and handled using Django's secure password hashing framework (no action required).
- To test:
  1. Start your virtual environment (if using one) and install dependencies (Django).
  2. Run migrations: `python manage.py makemigrations` and `python manage.py migrate`.
  3. Start server: `python manage.py runserver` and visit `/register/`, `/login/`, `/profile/`.

Customization
- To add profile pictures or extended profile fields, create a `Profile` model linked with a OneToOneField to `settings.AUTH_USER_MODEL`, add model forms and update templates.
