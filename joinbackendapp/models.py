import datetime
from django.db import models

from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length= 15)

    def __str__(self):
        return self.name
    
    
    
class Task(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(default=datetime.date.today)
    due_date = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
