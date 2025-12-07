from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="registration/logged_out.html"), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),

    # Post CRUD
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("posts/new/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    # Backwards-compatible singular routes (some clients or links expect these)
    path("post/new/", views.PostCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update_singular"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete_singular"),
]
