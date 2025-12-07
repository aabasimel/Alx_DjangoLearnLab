from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileForm


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
			return redirect("index")
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
