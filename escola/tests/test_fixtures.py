from django.test import TestCase
from escola.models import Estudante, Curso

class FixturesTestCase(TestCase):
    fixtures = ['escola/fixtures/prototipo_banco.json']
    
    def test_carregamento_da_fixtures(self):
        '''Teste que verifica o carregamento da fixtures'''
        #capturando as informações da fixtures -> ex: cpf da estudante Lorena Martins
        estudante = Estudante.objects.get(cpf="96730921170")
        #capturando as informações da fixtures -> ex: código do curso "como ganhar dinheiro"
        curso = Curso.objects.get(pk=1) 
        #conferindo celular do estudante
        self.assertEqual(estudante.celular, "43 96469-4621") 
        #conferindo o código do curso
        self.assertEqual(curso.codigo, 'como ganhar dinheiro') 