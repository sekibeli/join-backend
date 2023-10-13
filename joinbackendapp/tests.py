from django.test import TestCase
from django.test import Client
from django.test import TestCase
import unittest
from django.contrib.auth.models import User


class backendTest(TestCase):
    
    def test_login(self): 
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
