from django.db import models
from django.conf import settings


class Tag(models.Model):
	"""Simple Tag model for categorizing posts."""
	name = models.CharField(max_length=50, unique=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class Post(models.Model):
	"""A simple blog post model."""
	title = models.CharField(max_length=200)
	content = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
	)
	tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

	class Meta:
		ordering = ["-published_date"]

	def __str__(self):
		return self.title
