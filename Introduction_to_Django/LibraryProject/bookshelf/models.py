from django.db import models
import uuid

# Create your models here.
class Book(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=100)
    publication_year=models.IntegerField()