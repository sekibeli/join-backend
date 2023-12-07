from django.test import TestCase
from django.test import Client
from django.test import TestCase
import unittest
from django.contrib.auth.models import User
from rest_framework import status


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



   