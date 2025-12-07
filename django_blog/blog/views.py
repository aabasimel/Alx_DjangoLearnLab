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
from django.db.models import Q


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
		# Let the base class save the instance
		response = super().form_valid(form)
		# handle tags if form saved them to _tag_objs when commit=False
		if hasattr(form, "_tag_objs"):
			self.object.tags.set(form._tag_objs)
		else:
			# attempt to set from cleaned_data
			tags_str = form.cleaned_data.get("tags", "")
			if tags_str:
				tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
				from .models import Tag

				tag_objs = [Tag.objects.get_or_create(name=n)[0] for n in tag_names]
				self.object.tags.set(tag_objs)
		return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = "blog/post_form.html"

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author
    
	def form_valid(self, form):
		response = super().form_valid(form)
		# update tags from form
		tags_str = form.cleaned_data.get("tags", "")
		if tags_str is not None:
			tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
			from .models import Tag

			tag_objs = [Tag.objects.get_or_create(name=n)[0] for n in tag_names]
			self.object.tags.set(tag_objs)
		return response


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = "blog/post_confirm_delete.html"
	success_url = reverse_lazy("blog:post_list")

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author


def posts_by_tag(request, tag_name):
	"""Show posts filtered by a tag name."""
	posts = Post.objects.filter(tags__name=tag_name).distinct()
	return render(request, "blog/post_list.html", {"posts": posts, "tag": tag_name})


def search(request):
	"""Search posts by title, content or tag name using 'q' query param."""
	q = request.GET.get("q", "").strip()
	results = Post.objects.none()
	if q:
		results = Post.objects.filter(
			Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)
		).distinct()
	return render(request, "blog/search_results.html", {"posts": results, "query": q})

