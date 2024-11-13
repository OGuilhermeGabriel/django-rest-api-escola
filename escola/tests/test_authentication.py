from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status

class AuthenticationUserTestCase(APITestCase):
    def setUp(self):
        #criando um super usuário-teste para testar as autenticações
        self.usuario = User.objects.create_superuser(username='admin', password= 'admin')
        #capturando a url de listar os ojbetos, baseada no basename 
        self.url = reverse('Estudantes-list')

    def test_autenticacao_user_com_credenciais_corretas(self):
        '''Teste que verifica a autenticação de um user com as credenciais corretas'''
        #autenticando o usuário 
        usuario = authenticate(username= 'admin', password= 'admin')
        #verificando se a autenticação deu certo ou não:
        #o dado não pode ser vazio e o no usuário será aplicada a condição de autenticado
        self.assertTrue((usuario is not None) and usuario.is_authenticated)

    def test_autenticacao_user_com_username_incorreto(self):
        '''Teste que verifica a autenticação de um user com o username incorreto'''
        #autenticando o usuário de forma incorreta
        usuario = authenticate(username= 'adn', password= 'admin')
        #O dado sairá errado => erro no username (False)
        self.assertFalse((usuario is not None) and usuario.is_authenticated)

    def test_autenticacao_user_com_password_incorreto(self):
        '''Teste que verifica a autenticação de um user com o password incorreto'''
        #autenticando o usuário de forma incorreta
        usuario = authenticate(username= 'admin', password= 'ad')
        #O dado sairá errado => erro no password (False)
        self.assertFalse((usuario is not None) and usuario.is_authenticated)   

    def test_requisicao_get_autorizada(self):
        '''Teste que verifica uma requisição GET autorizada'''
        #a rota "url" precisa ser autenticada... forçando a autenticação abaixo
        self.client.force_authenticate(self.usuario)
        #capturando uma variável "response" e simulando a requisição
        response = self.client.get(self.url)
        #comparando o número da response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

