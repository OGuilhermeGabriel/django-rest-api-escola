from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from escola.models import Estudante     
from escola.serializers import EstudanteSerializer

class EstudantesTestCase(APITestCase):
    fixtures = ['escola/fixtures/prototipo_banco.json']
    def setUp(self):
        self.usuario = User.objects.get(username= 'gui')
        self.url = reverse('Estudantes-list')
        self.client.force_authenticate(user= self.usuario)
        self.estudante_01 = Estudante.objects.get(pk=1)
        self.estudante_02 = Estudante.objects.get(pk=2)
    
    def test_requisicao_get_para_listar_estudantes(self):
        '''Teste de requisição GET'''
        #puxe o código de response para capturar a informação dos estudantes do GET    
        response = self.client.get(self.url) #(/estudantes/)
        #comparando o statuscode recebido do teste
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_requisicao_post_para_criar_um_estudante(self):
        """Teste de requisição POST para um estudante"""
        dados = {
            'nome':'teste',
            'email':'teste@gmail.com',
            'cpf':'82271917034',
            'data_nascimento':'2003-05-04',
            'celular':'11 99999-9999'
        }
        response = self.client.post(self.url,data=dados)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_requisicao_delete_um_estudante(self):
        """Teste de requisição DELETE um estudante"""
        response = self.client.delete(f'{self.url}2/')#/estudantes/2/ que eu quero deletar
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_requisicao_put_para_atualizar_um_estudante(self):
        """Teste de requisição PUT para um estudante"""
        dados = {
            'nome':'teste',
            'email':'testeput@gmail.com',
            'cpf':'42370866071',
            'data_nascimento':'2003-05-09',
            'celular':'11 88888-6666'
        }
        response = self.client.put(f'{self.url}1/',data=dados)
        self.assertEqual(response.status_code,status.HTTP_200_OK)