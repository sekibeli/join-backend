from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Task, Category, Contact
from .serializers import TaskSerializer, CategorySerializer, ContactSerializer

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        
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