from django.test import TestCase
from django.test import Client
from django.test import TestCase
import unittest
from django.contrib.auth.models import User
from rest_framework import status
from .models import Task
from rest_framework.test import APIClient

class backendTest(TestCase):
    
    # def test_login(self): 
    #     response = self.client.post('/login/')
    #     self.assertEqual(response.status_code, 200)

    def test_login_success(self):
    # Benutzer erstellen, der für den Login verwendet wird
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        user.save()

    # Daten für die Login-Anfrage
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
         }

    # POST-Anfrage an die LoginView senden
        response = self.client.post('/login/', login_data)

    # Überprüfen, ob der Statuscode 200 OK ist
        self.assertEqual(response.status_code, 200)

    # Optional: Überprüfen, ob ein Token in der Antwort enthalten ist
        self.assertIn('token', response.data)
        
        
class TaskViewTest(TestCase):
    def setUp(self):
        # Testbenutzer erstellen
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Test-Tasks erstellen
        Task.objects.create(title="Task 1", description="Do task 1", author=self.user)
        Task.objects.create(title="Task 2", description="Do task 2", author=self.user)
        Task.objects.create(title="Task 3", description="Do task 3", author=self.user)

    def test_get_queryset(self):
        # Testen, ob die richtigen Tasks für den Benutzer zurückgegeben werden
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.objects.filter(author=self.user).count())

    def test_perform_create(self):
        # Testen, ob ein neuer Task mit dem authentifizierten Benutzer als Autor erstellt wird
        response = self.client.post('/tasks/', {'title': 'New Task', 'description': 'Do new task'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.last().author, self.user)

    def test_partial_update(self):
        # Testen des Teilupdates eines Tasks
        task = Task.objects.first()
        response = self.client.patch(f'/tasks/{task.id}/', {'title': 'Updated Task'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')



   