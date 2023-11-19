from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework import viewsets
from .models import Status, Task, Category, Contact, Subtask, Priority
from .serializers import SubtaskSerializer, TaskSerializer, CategorySerializer, ContactSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework import status




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
        # serializer = PrioritySerializer(priorities, many=True)
        # return Response(serializer.data)   
        return priorities    
        
        
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
    
    @action(detail=False, methods=['put'])
    def update_many(self, request):
        subtasks_data = request.data
       
        if not isinstance(subtasks_data, list):
            return Response({'error': 'Expected a list of items but got type {}'.format(type(subtasks_data).__name__)}, 
                            status=status.HTTP_400_BAD_REQUEST)

        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id')
            try:
                subtask = Subtask.objects.get(id=subtask_id)
                for attr, value in subtask_data.items():
                    if attr == 'task':
                        # Überprüfen, ob das Task-Objekt existiert und es dann zuweisen
                        task = get_object_or_404(Task, id=value)
                        setattr(subtask, attr, task)
                    else:
                        setattr(subtask, attr, value)
                subtask.save()
            except Subtask.DoesNotExist:
                return Response({'error': 'Subtask with id {} not found'.format(subtask_id)},
                                status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Subtasks updated successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_subtasks(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        # task = self.get_object()
        subtasks_data = request.data
        print(task)
        print(subtasks_data)
       
        # Subaufgaben verarbeiten und speichern
        # subtasks_data = task_data.get('subtasks', [])
        subtasks = []
        for subtask_info in subtasks_data:
            subtask = Subtask(
                task=task,
                title=subtask_info.get('title', ''),
                completed=subtask_info.get('completed', False)
            )
            subtask.save()
            subtasks.append(subtask)

        return Response({'status': 'subtasks added'}, status=status.HTTP_201_CREATED)

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
            category_data = task_data.get('category', [])
                                        
            try:
                category = Category.objects.get(id=category_data)
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category does not exist'}, status=400)

            priority_value = task_data.get('priority', '')
             # Überprüfen, ob der Wert von priority_value in Priority.choices vorhanden ist.
            if not priority_value in Priority.values:
                return JsonResponse({'error': 'Invalid priority value'}, status=400)
            

            # Stelle sicher, dass assigned_data immer eine Liste ist
            assigned_data = task_data.get('assigned', [])

            status_data = task_data.get('status', '')
            if not status_data in Status.values:
                return JsonResponse({'error': 'Invalid status value'}, status=400)
           # status = Status.objects.get(title=status_data) 
            
            # Erstelle die Task-Instanz und setze die anderen Felder
            task = Task.objects.create(
                title=task_data['title'],
                description=task_data['description'],
                category=category,
                dueDate=task_data['dueDate'],
                priority=priority_value,
                status=status_data,
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