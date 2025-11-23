from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')