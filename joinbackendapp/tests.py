from django.test import TestCase
from django.test import Client
from django.test import TestCase
import unittest
from django.contrib.auth.models import User
from rest_framework import status


class backendTest(TestCase):
    
    def test_login(self): 
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        # Benutzer für den Test erstellen
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.save()

    def test_user_view_authenticated(self):
        # Benutzer für den Test authentifizieren
        self.client.login(username='testuser', password='12345')

        # URL für die UserView anpassen
        url = '/path/to/your/user/view/'  # URL Ihrer UserView anpassen

        # GET-Anfrage an die UserView
        response = self.client.get(url)

        # Überprüfen, ob der Statuscode 200 OK ist
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Optional: Überprüfen der Antwortdaten
        # (abhängig von der Struktur Ihrer UserSerializer-Daten)
        # Beispiel: self.assertEqual(response.data['username'], self.user.username)