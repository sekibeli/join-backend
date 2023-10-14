from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

# Create your views here.
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
 
    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset