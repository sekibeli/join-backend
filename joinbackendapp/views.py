from django.shortcuts import render
from rest_framework import viewsets
from .models import Task, Category, Contact
from .serializers import TaskSerializer, CategorySerializer, ContactSerializer

# Create your views here.
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
 
    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset
    
class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
 
    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset
    
class ContactView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
 
    def get_queryset(self):
        queryset = Contact.objects.all()
        return queryset