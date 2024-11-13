from django.test import TestCase
from escola.models import Estudante, Curso, Matricula 

class ModelEstudanteTestCase(TestCase):
    def setUp(self):
        self.estudante = Estudante.objects.create(
            nome = 'Teste de Modelo',
            email = 'testedemodelo@gmail.com',
            cpf = '95197262095',
            data_nascimento = '2023-02-02',
            celular = '84 99999-9999'
        )
    
    def test_verifica_atributos_de_estudantes(self):
        '''Teste que verifica os atributos do modelo de estudante'''

        self.assertEqual(self.estudante.nome, 'Teste de Modelo')
        self.assertEqual(self.estudante.email, 'testedemodelo@gmail.com')
        self.assertEqual(self.estudante.cpf, '95197262095')
        self.assertEqual(self.estudante.data_nascimento, '2023-02-02')
        self.assertEqual(self.estudante.celular, '84 99999-9999')

class ModelCursoTestCase(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            codigo = 'ABCD123',
            descricao = 'Uma breve descrição do curso',
            nivel = 'I'
        )

    def test_verifica_atributos_de_cursos(self):
        '''Teste que verifica os atributos do modelo de cursos'''

        self.assertEqual(self.curso.codigo, 'ABCD123')
        self.assertEqual(self.curso.descricao, 'Uma breve descrição do curso')
        self.assertEqual(self.curso.nivel, 'I')

class ModelMatriculaTestCase(TestCase):
    def setUp(self):
        
        #criando obj de estudante-teste para a matrícula
        self.estudante_matricula = Estudante.objects.create(
            nome = 'Teste de Modelo Matricula',
            email = 'testedemodelo@gmail.com',
            cpf = '95197262095',
            data_nascimento = '2023-02-02',
            celular = '84 99999-9999'
        )

        #criando o objeto de curso-teste da matricula
        self.curso_matricula = Curso.objects.create(
            codigo = 'ABCD123',
            descricao = 'Uma breve descrição do curso',
            nivel = 'I'
        )

        self.matricula = Matricula.objects.create(
            estudante = self.estudante_matricula,
            curso = self.curso_matricula,
            periodo = 'M'
        )
    
    def test_verifica_atributos_de_matriculas(self):
        '''Teste que verifica os atributos do modelo de cursos'''

        self.assertEqual(self.matricula.estudante.nome, 'Teste de Modelo Matricula')
        self.assertEqual(self.matricula.curso.descricao, 'Uma breve descrição do curso')
        self.assertEqual(self.matricula.periodo, 'M')  