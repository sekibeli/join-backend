from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Task, Category, Contact
from .serializers import TaskSerializer, CategorySerializer, ContactSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated




# Create your views here.

class LoginView(APIView):
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
       
        if user:
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            return Response({
                'token': token.key,
                'user_id': user.pk
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
        current_user = self.request.user #eingloggten user holen
        if current_user.is_authenticated:
            return Task.objects.filter(author=current_user)
        return Task.objects.none()
       
    
class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
 
    def get_queryset(self):
       current_user = self.request.user #eingloggten user holen
        
       if current_user.is_authenticated:
            return Category.objects.filter(author=current_user)
       return Category.objects.none()
    
class ContactView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
 
    def get_queryset(self):
        current_user = self.request.user #eingloggten user holen
        
        if current_user.is_authenticated:
            return Contact.objects.filter(author=current_user)
        return Contact.objects.none()