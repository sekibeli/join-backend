import datetime
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.
class Priority(models.TextChoices):
        LOW = 'low'
        MEDIUM = 'medium'
        URGENT = 'urgent'

class Status(models.TextChoices):
           todo = 'To do'
           inProgress = 'In Progress' 
           awaitingFeedback = 'Awaiting Feedback'
           done = 'Done'

    
class Contact(models.Model):
    name = models.CharField(max_length=200)
    initials = models.CharField(max_length=3, blank=True, null=True)
    email= models.CharField(max_length=150)
    color = models.CharField(max_length=15)
    phone= models.CharField(max_length=150)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name
    
    def calculate_initials(self):
        names = self.name.split()
        initials = ''.join([name[0].upper() for name in names if name])
        return initials
        
    def save(self, *args, **kwargs):
        self.initials = self.calculate_initials()
        super(Contact, self).save(*args, **kwargs)
        
class Category(models.Model):
    title = models.CharField(max_length=100)
    color = models.CharField(max_length= 15)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.id}. {self.title}' 
    
    
class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created = models.DateField(default=datetime.date.today)
    dueDate = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    assigned = models.ManyToManyField(Contact, related_name='tasks', blank=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.LOW)
    status =  models.CharField(max_length=30,choices=Status.choices, default=Status.todo)
    
    def __str__(self):
        return self.title   

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks') 
    title= models.CharField(max_length=500)
    completed=models.BooleanField(default= False)
    
    def __str__(self):
        return self.title