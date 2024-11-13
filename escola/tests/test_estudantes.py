from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class EstudantesTestCase(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_superuser(username='admin', password= 'admin')
        self.url = reverse('Estudantes-list')
        #force a autenticação já no ambiente de teste definido por "setUp"
        self.client.force_authentication(user= self.usuario)