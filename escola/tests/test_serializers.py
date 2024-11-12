from django.test import TestCase
from escola.models import Estudante, Curso, Matricula
from escola.serializers import EstudanteSerializer, CursoSerializer, MatriculaSerializer

class SerializerEstudanteTestCase(TestCase):
    def setUp(self):
        #OBS: não precisa criar um novo obj para estudante, basta apenas instânciar o quem do teste da model de estudante
        self.estudante = Estudante(
            nome = 'Teste de Modelo',
            email = 'testedemodelo@gmail.com',
            cpf = '95197262095',
            data_nascimento = '2023-02-02',
            celular = '84 99999-9999'
        )
        #informe qual é o serializer que será aplicado o teste 
        self.serializer_estudante = EstudanteSerializer(instance= self.estudante)
    
    def teste_verifica_campos_serializados_de_estudantes(self):
        '''Teste que verifica os campos que estão sendo serializados de estudante'''
        #capturando os dados dos campos serializados  
        dados = self.serializer_estudante.data
        #capturando os campos (keys) com o objeto de estudante criado
        self.assertEqual(set(dados.keys()), set(['id','nome','email','cpf','data_nascimento','celular']))
    
    def teste_verifica_conteudo_dos_campos_serializados_de_estudantes(self):
        '''Teste que verifica o conteúdo dos campos que estão sendo serializados de estudante'''
        #capturando os dados dos campos serializados 
        dados = self.serializer_estudante.data 
        #capturando o conteúdo campos com o objeto de estudante criado
        self.assertEqual(dados['nome'], self.estudante.nome)
        self.assertEqual(dados['email'], self.estudante.email)
        self.assertEqual(dados['cpf'], self.estudante.cpf)
        self.assertEqual(dados['data_nascimento'], self.estudante.data_nascimento)
        self.assertEqual(dados['celular'], self.estudante.celular)

class SerializerCursoTestCase(TestCase):
    def setUp(self):
        self.curso = Curso(
            codigo = 'ABCD123',
            descricao = 'Uma breve descrição do curso',
            nivel = 'I'
        )
        self.serializer_curso = CursoSerializer(instance= self.curso)

    def teste_verifica_campos_serializados_de_cursos(self):
        '''Teste que verifica os campos que estão sendo serializados de curso'''
        dados = self.serializer_curso.data 

        self.assertEqual(set(dados.keys()), set(['id', 'codigo', 'descricao', 'nivel']))       

    def teste_verifica_conteudo_dos_campos_serializados_de_cursos(self):
        '''Teste que verifica o conteúdo dos campos que estão sendo serializados de curso'''
        dados = self.serializer_curso.data 

        self.assertEqual(dados['codigo'], self.curso.codigo)
        self.assertEqual(dados['descricao'], self.curso.descricao)
        self.assertEqual(dados['nivel'], self.curso.nivel) 

class SerializerMatriculaTestCase(TestCase):
    def setUp(self):
        self.estudante_matricula = Estudante.objects.create(
            nome = 'Teste Modelo Matricula',
            email='testemodelomatricula@gmail.com',
            cpf='91546870040',
            data_nascimento='2003-02-02',
            celular='84 99999-9999'
        )

        self.curso_matricula = Curso.objects.create(
            codigo = 'ABCD123',
            descricao = 'Uma breve descrição dos cursos',
            nivel = 'B'  
        )

        self.matricula = Matricula.objects.create(
            estudante = self.estudante_matricula,
            curso = self.curso_matricula,
            periodo = 'M'
        )

        self.serializer_matricula = MatriculaSerializer(instance= self.matricula)

    def teste_verifica_campos_serializados_de_matriculas(self):
        '''Teste que verifica os campos que estão sendo serializados de matricula'''
        dados = self.serializer_matricula.data

        self.assertEqual(set(dados.keys()), set(['id','estudante','curso','periodo']))

    def teste_verifica_conteudo_dos_campos_serializados_de_matriculas(self):
        '''Teste que verifica o conteúdo dos campos que estão sendo serializados de curso'''
        dados = self.serializer_matricula.data

        self.assertEqual(dados['estudante'], self.matricula.estudante.id)
        self.assertEqual(dados['curso'], self.matricula.curso.id)
        self.assertEqual(dados['periodo'], self.matricula.periodo)