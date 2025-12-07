from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileForm, PostForm
from .models import Post
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


def index(request):
	"""Simple index view for the blog home page."""
	return render(request, "blog/index.html")


def register(request):
	"""Handle user registration using the RegistrationForm."""
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			# Log the user in after successful registration
			login(request, user)
			return redirect("blog:index")
	else:
		form = RegistrationForm()
	return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
	"""Allow authenticated users to view and edit their profile."""
	if request.method == "POST":
		form = ProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return render(request, "registration/profile.html", {"form": form, "saved": True})
	else:
		form = ProfileForm(instance=request.user)
	return render(request, "registration/profile.html", {"form": form})


class PostListView(ListView):
	model = Post
	template_name = "blog/post_list.html"
	context_object_name = "posts"
	queryset = Post.objects.select_related("author").all()


class PostDetailView(DetailView):
	model = Post
	template_name = "blog/post_detail.html"
	context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = "blog/post_form.html"

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = "blog/post_form.html"

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = "blog/post_confirm_delete.html"
	success_url = reverse_lazy("blog:post_list")

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

