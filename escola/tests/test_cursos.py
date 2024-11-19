from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from escola.models import Curso
from escola.serializers import CursoSerializer

class CursosTestCase(APITestCase):
    fixtures = ['escola/fixtures/prototipo_banco.json']
    
    def setUp(self):
        #self.usuario = User.objects.create_superuser(username='admin', password= 'admin')
        self.usuario = User.objects.get(username= 'gui')
        self.url = reverse('Cursos-list')
        #force a autenticação já no ambiente de teste definido por "setUp"
        self.client.force_authenticate(user= self.usuario)
        #criando curso 01 
        self.curso_01 = Curso.objects.get(pk=1)
        #criando curso 02
        self.curso_02 = Curso.objects.get(pk=2)

    def test_requisicao_get_para_listar_cursos(self):
        '''Teste de requisição GET'''
        #puxe o código de response para capturar a informação do GET
        response = self.client.get(self.url)
        #comparando o statuscode recebido do teste
        self.assertEqual(response.status_code,status.HTTP_200_OK) 

    def test_requisicao_get_para_um_curso(self):
        """Teste para verificar a requisição GET para listar um curso"""
        #/cursos/1/
        response = self.client.get(self.url+'1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dados_curso = Curso.objects.get(pk=1)
        dados_curso_serializados = CursoSerializer(instance=dados_curso).data
        #print(dados_estudante_serializados)
        self.assertEqual(response.data, dados_curso_serializados)

    def test_requisicao_post_para_criar_curso(self):
        """Teste para verificar a requisição POST para criar um curso"""
        dados = {
            'codigo':'CTT3',
            'descricao':'Curso teste 3',
            'nivel':'A'
        }
        response = self.client.post(self.url,data=dados)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_requisicao_delete_para_deletar_curso(self):
        """Teste para verificar a requisição DELETE para deletar um curso"""
        response = self.client.delete(f'{self.url}2/')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_requisicao_put_para_atualizar_curso(self):
        """Teste para verificar a requisição PUT para atualizar um curso"""
        dados = {
            'codigo':'CTT1',
            'descricao':'Curso teste 1 atualizado',
            'nivel':'I'
        }
        response = self.client.put(f'{self.url}1/', data=dados)
        self.assertEqual(response.status_code, status.HTTP_200_OK)