from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework import viewsets
from .models import Status, Task, Category, Contact, Subtask, Priority
from .serializers import PrioritySerializer, SubtaskSerializer, TaskSerializer, CategorySerializer, ContactSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse




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
            return Response({'detail': 'Invalid credentials'}, status=http_status.HTTP_400_BAD_REQUEST)
        
class PriorityListView(APIView):
    def get(self, request):
        priorities = Priority.choices  # Holt alle Wahlmöglichkeiten des Priority-Enums
        serializer = PrioritySerializer(priorities, many=True)
        return Response(serializer.data)       
        
        
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
        current_user = self.request.user #eingloggten user holen
        if current_user.is_authenticated:
            return Task.objects.filter(author=current_user)
        return Task.objects.none()
    
    def perform_create(self, serializer):
        """Create a new task."""
        task = serializer.save(author=self.request.user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
        
    # PUT überschreiben
    
   # priority = Priority.objects.find(title = self....)
    
    
       
    
class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
 
    def get_queryset(self):
       current_user = self.request.user #eingloggten user holen
        
       if current_user.is_authenticated:
            return Category.objects.filter(author=current_user)
       return Category.objects.none()
   
    def perform_create(self, serializer):
            serializer.save(author=self.request.user)
             
class ContactView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
 
    def get_queryset(self):
        current_user = self.request.user #eingloggten user holen
        
        if current_user.is_authenticated:
            return Contact.objects.filter(author=current_user).order_by('name')
        return Contact.objects.none()
    
class SubtaskView(viewsets.ModelViewSet):
    serializer_class = SubtaskSerializer
    
    def get_queryset(self):
        current_user = self.request.user #eingloggten user holen
        subtask_ids = self.request.query_params.getlist('ids[]')  # Holt die Liste von IDs aus den Query-Parametern
        
        if current_user.is_authenticated:
            if subtask_ids:
                return Subtask.objects.filter(id__in=subtask_ids)  # Filtert Subtasks basierend auf den übergebenen IDs
            return Subtask.objects.all()  
        return Subtask.objects.none()
    

class AssignedView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    
    def get_queryset(self):
        current_user = self.request.user #eingloggten user holen
        contact_ids = self.request.query_params.getlist('ids[]')  # Holt die Liste von IDs aus den Query-Parametern
        
        if current_user.is_authenticated:
            if contact_ids:
                return Contact.objects.filter(id__in=contact_ids)  # Filtert Subtasks basierend auf den übergebenen IDs
            return Contact.objects.all()  # Oder irgendeine andere Standardlogik, die Sie möchten
        return Contact.objects.none()
       
class CreateTaskWithSubtasks(APIView):
   
    def post(self, request):
        current_user = self.request.user
        if request.method == 'POST':
            task_data = request.data

            # Zuerst die Kategorie und Priorität aus den Daten extrahieren
            category_data = task_data.get('category', {})
            priority_data = task_data.get('priority', '')
           
            # Kategorie und Priorität aus den Daten extrahieren und erstellen
            # try:
            #     category = Category.objects.get(id=category_data['id'])
            # except Category.DoesNotExist:
            #     print('Category existiert nicht')
            # priority = Priority.objects.get(title=priority_data)
            
            try:
                category = Category.objects.get(id=category_data['id'])
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category does not exist'}, status=400)

            priority_value = task_data.get('priority', '')
             # Überprüfen, ob der Wert von priority_value in Priority.choices vorhanden ist.
            if not priority_value in Priority.values:
                return JsonResponse({'error': 'Invalid priority value'}, status=400)
            

            # Stelle sicher, dass assigned_data immer eine Liste ist
            assigned_data = task_data.get('assigned', [])

            status_data = task_data.get('status', '')
            status = Status.objects.get(title=status_data) 
            
            # Erstelle die Task-Instanz und setze die anderen Felder
            task = Task.objects.create(
                title=task_data['title'],
                description=task_data['description'],
                category=category,
                dueDate=task_data['dueDate'],
                priority=priority_value,
                status=status,
                author=current_user,
            )

            # Verwende assigned_data, um die Many-to-Many-Beziehung festzulegen
            assigned_ids = [contact['id'] for contact in assigned_data]
            task.assigned.set(assigned_ids)

            # Subaufgaben verarbeiten und speichern
            subtasks_data = task_data.get('subtasks', [])
            subtasks = []
            for subtask_info in subtasks_data:
                subtask = Subtask(
                    task=task,
                    title=subtask_info.get('title', ''),
                    completed=subtask_info.get('completed', False)
                )
                subtask.save()
                subtasks.append(subtask)
         
            return Response(status=http_status.HTTP_201_CREATED)
        return Response(status=http_status.HTTP_400_BAD_REQUEST)

    def put(self, request, taskId=None):
        task_data = request.data