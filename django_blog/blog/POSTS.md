# Blog Post Management (CRUD)

This document describes the blog post CRUD features implemented in the `blog` app.

Overview
- ListView: shows all posts at `/posts/`.
- DetailView: shows a single post at `/posts/<pk>/`.
- CreateView: authenticated users can create posts at `/posts/new/`.
- UpdateView: only the author can edit their post at `/posts/<pk>/edit/`.
- DeleteView: only the author can delete their post at `/posts/<pk>/delete/`.

Permissions
- `PostCreateView` requires authentication (LoginRequiredMixin).
- `PostUpdateView` and `PostDeleteView` require the request user to be the post's author (UserPassesTestMixin).

Templates
- `blog/templates/blog/post_list.html` — list of posts.
- `blog/templates/blog/post_detail.html` — full post view.
- `blog/templates/blog/post_form.html` — used for create and edit.
- `blog/templates/blog/post_confirm_delete.html` — confirm delete.

Usage
1. Ensure migrations are applied and the server is running.
2. Visit `/posts/` to see all posts.
3. Login to create a post, or use the admin to create posts.
