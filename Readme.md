# Construindo uma API do zero

## Conhecendo Django Rest

### Construindo o ambiente virtual
> python -m venv venv

### Ativando o venv
> venv / scripts / activate

Vale salientar que caminho percorrido irá alterar à depender do sistema operacional
### Instalando as dependências

O ambiente virtual (venv) necessitará ser equipado com programas, arquivos e módulos atualizados que serão necessários para a execução do projeto. Todos estes conteúdos à serem baixados ou atualizados dentro do ambiente virtual são chamados de dependências.

OBS: Lembre-se de fazer isso sempre que você estiver com o ambiente virtual ativado

#### BOA PRÁTICA - requirements.txt 

Lembre-se de sempre que instalar novas dependências do projeto, atualizar o seu arquivo requirements.txt

> pip freeze > requirements.txt

#### Django 
> pip install Django

#### Django Rest Framework
OBS: Lembre de adicionar em settings > INSTALLED APPS: 'rest_framework',
> pip install djangorestframework

#### Django Rest Framework - MarkDown
markdown é um suporte para uma API mais navegável 
> pip install markdown

### Criando um projeto
> django-admin startproject setup . 

### Criando um app 
> python manage.py startapp [NOMEDOAPP]

### Conectando o aplicativo criado com o setup
Em setup > settings.py > na tupla INSTALLED_APPS, adicione:
> '[NOMEDOAPP]' ,

### Mudando a linguagem e o timezone
> LANGUAGE_CODE = 'pt-br'
> TIMEZONE = 'America/Sao_Paulo'

### Criando um GET usando JSON
No momento em que o usuário passar por esta rota, ele receberá uma informação vinda da API

Geralmente, podem ser feitas funções que tem como parâmetro essencial uma requisição(request) do tipo GET.

O JsonResponse importado e implementado na função serve para transformar todas as informações estelecidas na função "estudantes" (nesse caso, foi apenas um dict) em format JSON.

No caso desse projeto, o usuário recebe em uma rota específica, atravez de uma requisição GET da API, um dicionário contendo as informações básicas de um estudante específico.

Em views.py:
~~~
from django.http import JsonResponse

def estudantes (request):
    if request.method == 'GET':
        estudante = {
            'id':'1',
            'nome': 'guilherme'
        }
        return JsonResponse(estudante)
~~~

### Criando uma rota (path)
As informações que vem e vão de uma API por meio de requisições precisam estar relacionadas em uma rota. Por exemplo, Pra chegar do ponto A (API) para  o ponto B (usuário), um carro (a requisição) necessita de uma rota (path) para chegar de um ponto à outro.

Criamos e relacionamos estas rotas por meio das urls.py

1) Importe a requisição 
> from [NOMEDOAPP].views import estudantes

2) Adicione em url patterns o novo path
> path('estudantes/', estudantes),
> path('[ENDEREÇO DA REQUISIÇÃO]', CONTEÚDO DA REQUISIÇÃO),

Você pode conferir se a rota está funcionando indo para estudantes/ 

OBS: Não é uma forma muito eficiente, mas já é um começo. Com o framework do Django Rest, o negócio vai ficar melhor.

VANTAGEM: O DjangoRestFramework oferece uma serialização mais flexível e poderosa, permitindo um controle mais fino sobre como os dados são convertidos para JSON e vice-versa além de oferecer ferramentas que facilitam a construção de APIs, simplificando tarefas comuns como serialização de dados, roteamento de URLs e tratamento de requisições HTTP.

## Models e Serializers

### Models

Os models são os modelos referentes às tabelas do banco de dados. Entre outras palavras, o mapeamento de objetos relacionais (ORM) se dá pela relação entre classe que representa o model e o dataframe que representa o banco de dados. 

Dessa forma, estabecer atributos em uma classe de model é a mesma coisa que representar por meio do ORM, os campos relacionados do banco de dados. Tornando-se uma forma mais fácil de representar o banco de dados na minha API, tal como de manipula-lo, como veremos mais abaixo.

Ora, como o backlog do projeto pede como requisito para a API da escola os seguintes dados com id, nome, e-mail, etc. Todos eles serão atributos de uma classe de estudante em models.py da aplicação. Afinal, cada aplicação terá um model específico para ela, por mais que seja utilizada a mesma base de dados. Veja o exemplo de um model abaixo:

#### OBS - A questão do ID
O projeto pede para implementar o id, mas ele não foi declarado na models justamente por que o djangorestframework automaticamente colocará um id na tabela
~~~
class Estudante(models.Model):
    #os atributos da classe são os campos do meu dataframe
    nome = models.Charfield(max_lenght= 100)
    email = models.EmailField(blank=False, max_length= 30)
    cpf = models.Charfield(max_lenght= 11)
    data_nascimento = models.DateField()
    celular = models.Charfield(max_lenght= 14)

    #essa model/classe precisa retornar alguma coisa
    #nesse caso, retornará a string do nome do estudante
    def __str__(self):
        return self.nome
~~~

No caso desse projeto, além de uma model para os alunos, também foi feita para os cursos referentes à aplicação da escola.

#### OBS - Atributos com "choices"
Um ponto a ser salientado sobre a model de cursos é enteder como foi definido o atributo de níveis (básico, intermediário e avançado). Note que o usuário terá que selecionar qual dos níveis terá aquele curso. Dessa forma, faz-se necessário de um "choices" aqui para justamente, dar esta liberdade de escolha para o adm que fizer esta modificação.

Para isto, será criada uma tupla para para cada nível de curso, sendo cada par de tupla representado pela inicial (B) e o nome completo (Básico) do nível. Dessa forma, "B" será salvo no banco de dados (ocupando menos espaço) e "Básico" será a parte vísivel da aplicação que será implementada no template da página.

Além disso, toda vez que você implementar o "choices", coloque uma escolha padrão. Seja para dar prioridade ou para evitar espaços em blank.


~~~
nivel = models.CharField(max_length= 1, choices= NIVEL, blank= False, null= False, default= 'B')
~~~

#### OBS - Alterou alguma models ? Faça as migrations

Faça as migrações:
> python manage.py makemigrations

Migre as migrações: 
> python manage.py migrate

#### Admin
A sessão de admin da aplicação diz respeito à parte da aplicação dedicada ao administrador.
Como eu quero que a parte de admin tenha acesso ao alunos e cursos baseados no model. Torna-se necessário eu registrar os models em admin.py

Primeiramente, importe-os:
~~~
from <NOMEDOAPP>.models import <MODEL1>, <MODEL2>
~~~

Agora será necessário criar uma classe para registrar a model no admin:
~~~
class Estudantes(admin.ModelAdmin):
    #listando todos os parâmetros
    list_display= ('id','nome','email','cpf', 'data_nascimento','celular')
    #parametros "clickáveis"
    list_display_links= ('id','nome')
    #listagem por página
    list_per_page = 20 
    #opção pra pesquisar um campo em específico: nesse caso por nome
    search_fields = ('nome',)
~~~

Criada a classe da model no admin, registre a model no admin:
Como exemplo qualquer, criei a seguinte
> gui, 123
~~~
admin.site.register(Estudante, Estudantes)
admin.site.register(<MODEL>, <MODELDOADMIN>)
~~~

#### OBS - Models X json

Como visto anteriormente, o modelo criado em views tratasse de um único dicionário o qual atribuirá as informações dos estudantes. Note que, ao invés disso, é muito mais prático a implementação de Models no projeto, uma vez que eles são mais fáceis de manipular em escalas numéricas maiores uma vez que estamos utilizando o paradigma de orientação à objetos provido do python, sendo aplicado como ORM por meio do Django.

Portanto:
> Models > json

#### Criando um superusuário 
Para você poder acessar a parte de admin, primeiramente você precisa ter o acesso de um superuser.

> python manage.py createsuperuser

#### Acessando Admin
basta apenas colocar um /admin no final da url para ter acesso à página de administração do Django.

Dessa forma, por meio de uma interface, será mais fácil de realizar o CRUD manualmente
### Serializers
Da forma como atualmente está o projeto, as informações do banco de dados são levadas de forma cru para o usuário. Faz-se necessário então utilizar alguns métodos para aplicar os dados do banco de dados em um template mais elaborado vindo das views.

Agora, por meio dos models, todos os dados são armazenados no banco de dados e dentro do banco de dados eles são caracterizados como objetos complexos (queryset), que é nada mais nada menos do que uma instância dos models que estão sendo aplicados.

Nesse sentido vem os serializers, que são componentes responsáveis por converter os dados complexos em um datatype python, para que seja possível transformar o datatype para outro tempo que for conveniente para a aplicação: json, xml, etc.

#### Serielizers - fluxo de dados geral

![serializers_geral](/readme_assets/serializers_geral.jpg)

Fonte: https://www.alura.com.br/

Obs: As flechas rosas indicam um request (uma requisição) e as flechas brancas indicam um response (uma resposta).

Note que o serializer fica entre as views e as models. Ou seja, as respostas vindas por contas das requisições que passam pelas models, primeiramente passarão pelos serializers para converter o objeto complexo justamente para um datatype apropriado para que a view consiga interpretar os dados.

#### Serializer, Models, Database - fluxo de dados especifico

![serializers_database](/readme_assets/serializers_model_database.jpg)

Fonte: https://www.alura.com.br/

Como já mencionado, haverá uma comunicação entre os models e o database por meio do ORM, onde o models sempre estarão passando um dado do tipo queryset(instância do modelo ou objeto complexo) ou que eles enviam ou que eles recebem do banco de dados.

O serializador pega esses dados vindos dos models para as views e transforma num datatype python mais conveniente para ser trabalhado nas views.

Nessa sentido o serializer pode ser comportar como um filtro de dados. Uma vez que você pode filtrar as informações específicas que um model tem

#### Implementando serializers na aplicação - ModelSerializers
Vale salientar que serializer é uma classe geral manual, tornando-se possível serializer diversas coisas na aplicação. Para este ponto do projeto, será utilizado especificamente a classe ModelSerializer que é mais otimizada e será utilizada para validar os dados que passam entre models e views.

No caso desse projeto, serão serializadas as duas models referentes aos estudantes e aos cursos.

1) Crie um arquivo serializers.py dentro da pasta da sua aplicação
2) Dentro de serializers, importe o serializador geral e os models que serão serializados
3) Crie os serializers de cada model, que serão classes que tem como parâmetro as models
~~~
class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        #declarando a model que será serializada
        model = Estudante 
        #declarando os campos que o serializer irá pegar
        fields = ['id','nome','emai','cpf','data_nascimento','celular']
~~~
4) Teste a eficiência do serializer aplicado no shell do django via terminal
- Importe os models e os respectivos serializers que serão testados 
- Dentro de uma variável queryset, atribua a ela todas as instâncias de model (todos os dados criados por meio do banco de dados baseado na respectiva model)

~~~
#atribuindo valor ao queryset
queryset = <model>.objects.all()
#chamando o queryset, pra conferir todas as instâncias da respectiva model
queryset
~~~ 

- Dentro de uma variável serializer, atribua à ela a classe do serializer que você quer testar tendo como parâmetros o queryset do respectivo model. Depois disso, é só chamar a variável serializadora para testar se todos os dados vindos das models estão passando pelos serializers sem nenhum problema.

~~~
#fazendo a atribuição da variável serializadora
serializer = <classe_serializadora>(queryset, many= True)
#chamando a variável 
serializer.data
~~~
## Viewsets
O viewset (como o nome diz) é um set de views ou agrupamento de views que contém as operações CRUDs necessárias para implementação da API.
### Criando ModelViewsets
Serão utizados os modelviewsets para aplicar o viewset nos modelos da aplicação em views.py [ Se você ainda está com aquele exemplo de json em views, pode apagar ]

1) importe os models, os serializers e do rest framework, importe o viewsets também

2) Crie uma classe representar o viewset. Dentro dela, puxe todas as instâncias do model que foram pegas no viewset com o query
~~~
class EstudanteViewSet(viewsets.ModelViewSet):
    #em queryset, haverão todas as instâncias do model Estudante. Ou seja, todos os estudantes
    queryset = Estudante.objects.all()
    #atribuindo o serializer respectivo ao viewset, dado um model específico 
    serializer_class = EstudanteSerializer
~~~
### Configurando as URLs
Antes de configurar as URLs dos estudantes e dos cursos, faz se necessário configurar em setup, as urls do projeto como um todo. 

#### Configurando as URLs em setup - Routers

Note que pelo fato do código estar assim:
~~~
urlpatterns = [
    path('admin/', admin.site.urls),
    path('estudantes/', estudantes),
]
~~~
Toda vez que você adicionar uma nova URL, você terá que criar um novo path para ela e o código pode ficar bastante longo e poluído por causa disso. Dificultando até mesmo da fazer a manutenção à longo prazo.

Para otimizar esta situação, podemos utilizar a metodologia de routers disponibilizados pelo próprio framework.

- Classe Routers
Para resolver este caso, cria-se um objeto da classe router o qual irá armazenar todas as rotas de urls.py. Dessa foram, basta apenas inserir este objeto da classe router dentro de urlpatterns. Evitando assim a poluição visual e facilitando a manutenção das rotas. 

Nesse caso será utilizado o DefaultRouter pois será apartir dele que será criada uma interface que irá mostrar as interfaces para nós, pois ela cria automaticamente uma root view (view de rota) chamada API root

1) Em urls.py importe as ViewSets, o routers do rest_framework
2) Crie um objeto da classe defaultrouter chamado router
~~~
router = routers.DefaultRouter()
~~~
3) Registre as rotas que você deseja aplicando. Como parâmetros, passe o prefixo da rota, o viewset atrelado e o nome da rota. Por exemplo: 
~~~
router.register('estudantes',EstudanteViewSet,basename='Estudantes')
~~~
4) Vá em url patterns e adicione os routers registrados para o path, incluido o route (sim, precisa usar um "include" e para isso importe-a do django.urls)
~~~
path('', include(router.urls))
~~~

OBS: Essa " path('') " tratasse da rota inicial, aquela que aparecerá na primeira página. Essa primeira página será justamente a nossa API root, uma view de rotas vinda justamente da classe de router DefaultRouter. Tratasse basicamente de uma interface que mostrar as rotas disponíveis para serem acessadas dado o número de rotas que foram registradas usando router.register()

### Explorando o API root
Como já mencionado acima, o API root serve para realizar operações CRUD sem a necessidade de operar no admin. 

- Quero acessar uma instância já criada do meu model

Caso queira acessar os dados de algum estudante específico, basta apenas eu redirecionar a URL para router que você registrou com relação ao viewset respectivo ao model de estudantes.

> 367.3.0.1:8000/estudantes/2/

Note que o estudante que você irá busca é o do id = 2. Esta opção é por default.


OBS: Como pode notar, existem várias formas de você implementar operações de CRUD na API, podendo ser no API root, na página do Admin, ou em extensões que facilitem essa implementação como Thunder Client ou até mesmo softwares dedicados Insomnia REST, Postman API,etc.

Elas serve principalmente para que seja possível trabalhar com as requisições GET e POST.

#### Put, Patch e Delete
São requisições mais focadas em criar, deletar e atualizar os dados 

- Put

É uma requisição que o programador chama para realizar alterações em instâncias do modelo INTEIRO. Basta apenas você acessar tal instância, realizar as alterações e realizar a requisição.

- Patch

É uma requisição que o programador chama para realizar alterações em instâncias do modelo ESPECÍFICAS (geralmente aplica-se a requisição no formato JSON). Basta apenas você acessar tal instância, realizar as alterações e realizar a requisição.

- Delete

Sem redundância aqui. Basta apenas acessar a instância e deletar.

## Adicionando recursos na API
### Criando a model da matrícula
Assim como foi para os estudantes e para os cursos, será necessário criar um model, um viewset e um serializer para as matrículas.

Note que as model de matrícula deverá se relacionar com o model de Estudante (Se o estudante for deletado, todas as matrículas relacionadas à ele serão também deletadas) e com a model de Curso (Se o curso for deletado, todas as matrículas daquele curso serão deletadas).

Vale salientar também que as matrículas seguem um tipo de relacionamento com os estudantes e com os cursos chamado Many To One (Vários para um). Isso significa que um   único estudante pode ter várias matrículas de vários cursos, assim como um único curso pode ter várias matrículas para vários estudante. O contrário não irá acontecer, uma vez que só pode haver uma única matrícula associada à uma combinação de um aluno e um curso.

### Criando os recursos da matrícula

Dessa forma, pelo fato do relacionamento da matrícula com os alunos e os cursos serem Many To One, o DRF disponibiliza o ForeignKey que relaciona a classe  com a outra classe e o CASCADE delete que serve para que, ao deletar uma instância daquilo que está em ForeignKey, delete também a instância da matrícula 

1) Em models, crie um model para a matrícula
2) Obs: Dentro da classe de model da matrícula, note o seguinte: 
~~~
    #variável estudante recebe o método foreignkey o qual tem como parâmetros o model relacionado ao estudante e o on_delete CASCADE
    #pois caso o model de estudante seja deletado, a instância do model matrícula (a matrícula relacionada ao estudante) será deletada também
    estudante = models.ForeignKey(Estudante, on_delete= models.CASCADE)
~~~
3) Crie o serializer
4) Crie o viewset 
5) Crie um path (registrando uma nova instância de router)
6) Implemente a função no admin  (crie a classe de matrículas)

### Adicionado Serializer de listar a matrícula
Será criado agora 2 serializers: 

Um serializer para filtrar e dizer pro viewset que vai passar apenas os cursos e o período do estudante (serializer de matrícula por estudante). 

 O outro serializer é para filtrar e dizer pro viewset que vai passar apenas os nomes dos estudantes associados ao curso (serializer de matrícula por curso).

Para apenas mostrar os dados, será utilizado a classe de serializer field readonlyfield(), a qual serve apenas para retornar o valor daquele campo.

Será aplicado também o SerializerMethodField(), o qual vai criar um método que retornará um valor selecionado, que será um objeto (aluno ou curso, no caso) o qual será pego pela requisição GET.

Fazendo o serializer de matrícula por estudante, por exemplo:

~~~
class ListaMatriculaEstudanteSerializer(serializers.ModelSerializer):
    '''
    determinando o curso como um serializer só de leitura (do parâmetro descrição) e
    capturando o parâmetro exato do curso que será lido (descrição) 
    '''
    curso = serializers.ReadOnlyField(source= 'curso.descricao')
    #capturando o período pelo método "get_periodo"
    periodo = serializers.SerializerMethodField()
    class Meta:
        #model que eu vou puxar os campos
        model = Matricula
        #campos da model que serão usados 
        field = ['curso','periodo']
    
    '''
    criando o método para capturar o "período" da forma desejada (não a visível do
    banco de dados 'M', por exemplo)
    '''
    def get_periodo(self,obj):
        return obj.get_periodo_display()
~~~
### Adicionando recursos de listar matrículas
Ao invés de utilizar um viewset para as matrículas, serão criados agora views específicas ou para visualizar as matrículas do estudante ou as matrículas do curso. Nesse sentido, será utilizado uma extensão do GenericAPIView chamada de ListAPIView, que é usado apenas como read-only. 
Para isso, será necessário definir um método pra capturar todas as informações das models (get_queryset)

1) Em views.py, importe os serializers de listadematriculas e listadecursos 
2) Em rest_framework,  importe o generics 
3) Crie as classes de ListAPIView para cada uma dos 2 serializers
~~~
class ListaMatriculaEstudante(generics.ListAPIView):
    '''
    capturar o queryset, mas apenas um estudante específico. O estudante será identificado
    por meio do seu respectivo id. Logo, o queryset guardará o id
    '''
    def get_queryset(self):
        queryset = Matricula.objects.filter(estudante_id = self.kwargs['pk'])
        return queryset
    
    #definindo a classe do serializer
    serializer_class = ListaMatriculaEstudanteSerializer
~~~
4) Em urls.py crie a rota: importe a view, passe essa informação no path pois é uma informação específica
~~~
path('estudantes/<int:pk>/matriculas/',ListaMatriculaEstudante.as_view())
~~~

OBS: Faça o mesmo processo para a lista de cursos.
## Adicionando Autenticação na API
Da forma que atuamente estão, as listas de alunos e de cursos referentes as matrículas estão exercendo apenas a função de readonly, o que é adequadro para o projeto. O problema é referente ao path de estudantes e de cursos, onde qualquer pessoa no API root tem permissão para realizar alterações, diferentemente na sessão do admin que o usuário precisa passar pela autenticação de login e senha. Dessa forma, faz-se necessária a implementação de uma autenticação na API root para previnir isso.

Com isso, será apenas permitido o acesso às rotas da API para pessoas autenticadas. Nesse caso, uma pessoa autenticada é aquela que apresenta um usuário cadastrado no admin. Dessa forma, será utilizado o BasicAuthentication aplicando o IsAuthenticated, pois só vai permitir o acesso do usuário se ele estiver autenticado.

- Configurando a autenticação

1) Em views.py, importar o Basic Authentication e o IsAuthenticated
2) Aplique as autenticações nos viewsets desejáveis, colocando no início de cada classe de view:
~~~
authentication_classes = [BasicAuthentication]
permission_classes = [IsAuthenticated]
~~~

Dessa forma, pra cada view que você coloquei essa authenticação, irá pedir o login do admin para poder acessa-la. 
### Trabalhando com outras permissões

Ok, pode até existir essa autenticação de admin, mas nada impede que quem acessou o admin seja apenas um usuário que, em tese, não faz parte do grupo de membros responsáveis pelas operações de CRUD. Por tanto, faz-se necessário aplicar autenticações no admin para evitar esses problemas.

É possível aplicar outra permission (além do IsAuthenticated) voltada ao admin chamada de IsAdminUser. Note que para as diversas classes de views, é possível trabalhar com permissões diferentes. Ou seja, usuários diferentes possuem permissões diferentes para acessar determinados tipos de conteúdos contidos na API. É possível utilizar também o IsAuthenticatedOrReadOnly para as pessoas que estiverem com esse tipo de autenticação, consigam apenas ler. 

~~~
permission_classes = [IsAdminUser]
~~~
ou
~~~
permission_classes = [IsAuthenticatedOrReadOnly]
~~~

Dessa forma, para acessar algumas views, além de ter a autenticação via login, o tipo de usuário deverá ser um específico de membro responsável pelas operações de CRUD.

### Otimizando o código das autenticações
Note que agora, por questões de autenticação, todas as classes serializadoras terão o authentication_class e o permission_classes. Isso acaba deixando o código muito poluído. 

Essas informações podem ser generalizadas com o intuito de melhorar a organização do código. Dessa forma, basta apenas ir em settings.py e determinar estas classes globalmente:

~~~
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permission.IsAuthenticated',
    ]
}
~~~

Lembre-se de apagar os importes de permissão e autenticação em views.py, além de deleta-las para cada viewset. Pois agora, como as permissões e autenticações são globais, até mesmo para entrar na página inicial da API root, será necessário uma autenticação de login. 

# Validações, paginação, filtros e versionamento
## Criando Validações nos Models
Agora será necessário criar validações nas models para evitar erros de autenticação referente aos cadastros tanto dos alunos quanto dos cursos. Por exemplo, não é permitido cadastrar um aluno cujo cpf já tenha sido cadastrado em outro aluno.
### Definindo valor único de dados 
Nesse sentido, é atribuido para os parametros das models um valor único de dados o qual não irá se repetir para as outras instâncias de um determinado model. 

Dessa forma, existem várias formas de definir estes valores únicos. Nesse caso em especifico, será adicionado no atribudo "cpf" da classe de modelo de estudante o parâmetro unique, para verificar se é um dado único. Ou seja, em unique = True, o valor precisa ser único. Caso não seja, ele não será cadastrado.

~~~
    cpf = models.CharField(max_length= 11, unique= True)
~~~

A mesma metodologia pode ser aplicada no código de todas as instâncias da classe de model do curso.

É possível também adicionar validators para que haja além de um comprimento máximo (max_lenght), um comprimento mínimo do código.

1) Importe o minlenght validator do django.core.validators 
2) No código coloque o parametro validators
~~~
    codigo = models.CharField(max_length= 100, unique= True, validators= [MinLengthValidator(<QUANTIDADE_MINIMA>)])
~~~

## Validações no Serializer 

A validação no serializer é uma forma específica e acaba sendo mais aplicadas para casos específicos. Ou seja, para realizar validações customizadas (custom validators).

Por exemplo, podemos aplicar uma validação no cpf com um número máximo de pessoas. Nesse caso, será utilizado uma Field-Level validation, que seria um método aplicado na classe serializadora onde tal método irá retornar o valor autenticado.

- Validando o cpf pelo serializer do estudante
~~~
    def validate_cpf(self, cpf):
        #autenticação referente ao número de dígitos máximos do cpf
        if len(cpf) != 11:
            raise serializers.ValidationError('O CPF precisa ter no mínimo 11 ! ')
        #retornando o valor autenticado 
        return cpf
~~~

- Validando nome pelo serializer de estudante
~~~
    def validate_nome(self, nome):
        #caso o nome não seja alfanumérico (c/ caracteres especiais)
        if not nome.isalpha():
            #erro emitido
            raise serializers.ValidationError('O nome só pode ter letras ')
        #retorna o nome validado
        return nome
~~~

- Validando o número de celulares
~~~
    def validate_celular(self, celular):
        #caso o número de dígitos não seja 13 dígitos 
        if len(celular) != 13:
            raise serializers.ValidationError('O número de celular deve ter 13 dígitos')
        return celular
~~~

OBS: Note que, por mais que os métodos de validate sejam bastante eficientes, eles ocupariam bastante espaço à longo prazo. Para o código ficar mais organizado.

~~~
    def validate(self, dados):
        if len(dados['cpf']) != 11:
            raise serializers.ValidationError({'cpf':'O CPF precisa ter no mínimo 11 !'})
    
        if not dados['nome'].isalpha():
            raise serializers.ValidationError({'nome':'O nome só pode ter letras'})

        if len(dados['celular']) != 13:
            raise serializers.ValidationError({'celular':'O número de celular deve ter 13 dígitos'})
        
        return dados
~~~

Note que agora, no lugar de validate recebe vários campos separados, haverá apenas uma variável chamada dado que será em cada validação um dicionário respectivo um campo e a mensagem de erro direcionada ao campo.

Dessa foram, a sequência de validações será relevante. Por exemplo: caso ocorram erros de validações em todos os campos, o erro que aparecerá será o primeiro dessa "lista" de validators.

### Criando arquivos Validate
Note que, com o passar do tempo, a quantidade de validações irá aumentar à medida que inserirmos novos tipos de validações tal como novos serializers para a aplicação. Dessa forma torna-se, necessário aplicar uma nova abordagem para evitar tamanha poluição textual além de otimizar o processo de manutenção das próprias validações. 

Nesse sentido, por questões de boa prática, todas estas validações serão colocadas em um arquivo apenas de validação para que no serializer, baste apenas importar tal arquivo contendo as validações. 

1) Na pasta da aplicação, crie um novo arquivo chamado validators.py 

2) Coloque no arquivo as validações
~~~
#função que valida o cpf
def cpf_invalido(cpf):
    return len(cpf) != 11

#função que valida o nome
def nome_invalido(nome):
    return not nome.isalpha()

#função que valida o celular
def celular_invalido(celular):
    return len(celular) != 13
~~~

3) Em serializers.py, importe o arquivo de validators com as funções validators  
~~~
from escola.validators import cpf_invalido, nome_invalido, celular_invalido
~~~

4) Vá para a classe de serializers e na função de validação dos serializers, basta apena substituir a lógica que você fez para validar pela própria função validadora que foi importada do validators.py. Por exemplo, no validate do serializer do estudante: 

~~~
    def validate(self, dados):
        #função que tem como parâmetro o dicionado de "dados" com a chave selecionada do cpf
        if cpf_invalido(dados['cpf']):
            raise serializers.ValidationError({'cpf':'O CPF precisa ter no mínimo 11 !'})

        #função que tem como parâmetro o dicionado de "dados" com a chave selecionada do nome    
        if nome_invalido(dados['nome']):
            raise serializers.ValidationError({'nome':'O nome só pode ter letras'})

        #função que tem como parâmetro o dicionado de "dados" com a chave selecionada do celular
        if celular_invalido(dados['celular']):
            raise serializers.ValidationError({'celular':'O número de celular deve ter 13 dígitos'})
        
        return dados
~~~

Note que dado é uma única variável responsável por armazenas as informações dos outros registros como cpf, celular, etc. É importante salientar isso pois declarar apenas uma variável para a função acaba facilitando a escrita do código e acaba se tornando uma boa prática. 

## Importando validações e gerando clientes

### Trabalhando com Regex
Existem certos tipos de validações em que será necessário identificar um comportamento ou um padrão. Para isso, será necessário utilizar expressões regulares (Regular Expressions), também conhecido como regex. Os regex basicamente irão criar um padrão de busca para validar algo. 

Por exemplo, checar um número de celular apenas pela quantidade de dígitos não será o suficiente para saber se o número é válido. Sabendo que um número deveria seguir um seguinte formato, respeitando caracteres, espaços e traços: 

> DD 12345-6789

Para identificar esse formato/expressão, será necessário utilizar o regex.

1) Em validators, importe o regex
2) Dentro de uma das funções de validação, indique o modelo que você quer regular
3) Aplique o regex para você comparar o dado específico com o modelo, armazenando o resultado numa variável. A título de exemplo:
~~~
def celular_invalido(celular):
    # DD 12345-6789
    modelo = f'[0-9]{2} [0-9]{5}-[0-9]{4}'
    # comparando o modelo 
    resposta = re.findall(modelo, celular)
    return not resposta
~~~
Caso o dado atenda os requisitos do modelo, será retornado para a variável "resposta" uma lista com o dado que será recebido. Caso não seja, a resposta receberá uma lista vazia. Logo, a função retorna "not resposta" uma vez que a função só será chamada caso o dado não estiver de acordo com o modelo. Ou seja, para o exemplo acima, a função só será chamada quando o dado referênte ao celular for inválido. 

### Importando Validações
Validar um cpf, por exemplo, é muito mais complexo deo que simplesmente exigir que o campo tenha X caracteres. A legislação e as leis do Brasileiras definem como ele é constituido e criam até um algoritmo para gerá-lo. 

Dessa forma, ao invés de pegar este algoritmo e aplicá-lo no projeto, torna-se mais interessante importar uma biblioteca do python que valida não só o cpf mas também outros documentos brasileiros. A biblioteca que será importada nesse caso será a validate-docbr

1) Dentro do ambiente virtual, instale a biblioteca
> pip install validate-docbr
2) Boa prática, coloque essa informação dentro do arquivo requirements.txt
> pip freeze > requirements.txt
3) No validators.py, importe os validators da biblioteca e aplique na função de validação
~~~
def cpf_invalido(numero_cpf):
    #uma variável para a função que valida o cpf (CPF)
    cpf = CPF()
    #chamando o metodo de validação do cpf para a variável "cpf válido"
    cpf_valido = cpf.validate(numero_cpf)
    #como a função de validação é ativado caso o dado esteja invalido, retorne o dado invalido
    return not cpf_valido
~~~
4) Lembre-se de realizar as alterações necessárias no serializer também, como a mensagem que será exibida no campo que estiver inválido.

## Incluindo paginação, ordenação e filtros
### Preparando o ambiente - Populando o banco de dados da API
Para testar operações como paginação, ordenação e filtros será necessário que haja um banco de dados populado com informações o suficientes para que a API consiga realizar as seguintes operações. Contudo, pelo fato desta aplicação ainda não ter uma quantidade significativa de dados, será necessário trabalhar com dados simulados, criando vários dados simulados. 

Como usei como base os cursos da alura, eu peguei os arquivos de template referente ao banco de cursos e ao banco de alunos que foram disponibilizados durante o curso e utilizei a biblioteca Faker para gerar os dados falsos de maneira mais fácil e eficiente.

1) Baixe os scripts de para popular 
2) Coloque no mesmo nível do diretório do manage.py
3) Para executar estes scripts, instale a biblioteca do fake 
> pip install Faker
Logo após:
> pip freeze > requirements.txt
4) Abra o terminal e lá, execute os scripts 
> python popular_banco_cursos.py
> python popular_banco_estudantes.py

Agora o banco de dados está populado.

### Adicionando paginação
A paginação será um elemento de organização de dados na API a qual fará com que uma quantidade "X" de dados seja separados por uma quantidade "n" de dados por página. Dessa forma, a experiência do usuário torna-se mais prática além do site carregar mais rápido pois, ao invés da página demorar para carregar todos os 1000 estudantes, basta apenas utilização uma paginação onde apenas seriam exibidos 20 estudantes por página. Existem vários tipos de páginações, a utilizada para este projeto foi a paginação por páginas, que é a PageNumberPaginationl. 

Vale salientar que os dados que me refiro são justamente os objetos/instâncias criadas por meio das models referentes nesse caso aos estudantes, cursos e matrículas registradas na API. 

- Configuração global

Configurar o PageNumberPagination para todas as rotas da API. Em setup, settings.py, No dicionário do REST_FRAMEWORK:
~~~
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    #Quantidade de dados por página
    'PAGE_SIZE': 20
~~~
### Incluindo ordenação
Ordenação é um filtro aplicado para saber a ordem em que os dados estão disponibilizados para a visualização do usuário da API. Inicialmente, a ordenação estabelecida de forma padrão foi de acordo com os Id's dos objetos. Para o projeto, serão ordenados os dados da rota de estudante pelo parâmetro de nome.

Antes de aplicar qualquer filtro, será necessário configurar a biblioteca DjangoFilterBackend, necessária para a implementação não só da ordenação para os demais filtros a serem aplicados no projeto. 

1) Instale a biblioteca: 
> pip install django-filter 
OBS:
> pip freeze > requirements.txt
2) Adicione "django_filters" dentro do INSTALLED_APPS em settings, caso queira instalar os filtros de forma global
3) Adicione a configuração dos filtros na views.py da aplicação:
- Importe o DjangoFilterBackend e o filters 
- Dentro do viewset ou da view desejável, adicione os filtros 
~~~
class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all()
    serializer_class = EstudanteSerializer
    #baseado no DjangoFilterBackend, defina o tipo de filtro (nesse caso: OrderingFilter)
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    #O campo que será ordenado
    ordering_fields = ['nome']
~~~
4) É possível também colocar o filtro de ordenação no admin. Em admin.py, na classe de estudante:
~~~
ordering = ('nome',)
~~~
### Adicionando filtros de busca
Agora criaremos dois filtros de busca: Um filtro de cpf no admin e um filtro para buscar por parâmetro o qual pode ser por nome e/ou cpf. 

- Implementando mais filtros de busca no admin

O primeiro filtro de busca é tranquilo e intuitivo de se fazer. Basta apenas ir no admin.py da aplicação, e em "searching fields" da classe referente aos objetos que você quer implementar (estudante, curso, matrícula, etc) e adicionar o parâmetro de cpf.

~~~
search_fields = ('nome', 'cpf')
~~~

- Implementando filtros de busca na API 

Para isso, será utilizado para a aplicação o SearchFilter onde, por meio dela, será implementado uma barra de busca na API root. Será por meio dessa barra de busca que o usuário entrará com um parâmetro específico e ele retornará uma lista de dados relacionados à tal parâmetro. Note logo abaixo que o processo de implementação do filtro de busca é similar com o de ordenação.

Em views.py, na classe remetente aos objetos que você quer filtrar:
1) Em filters_backends, adicione o tipo de filtro "filtro de busca" o qual será aplicado
~~~
filter_backends = [DjangoFilterBackend, filters.SearchFilter]
~~~
2) Indique os campos que serão filtrados no campo de busco 
~~~
search_fields = ['nome','cpf']
~~~
## Criando outras versões

### Trabalhando com o versionamento 
O versionamento de uma API é um prática essencial para o desenvolvimento do projeto como um todo: seja para realizar manuteções ou para facilitar a implementação vinda por terceiros. 

Para este caso, a aplicação passará por uma migração de sistema onde uma nova versão do sistema será implementada. Nesse sentido, será aplicado o conceito de versionamento para que ocorra a migração da versão 1 para a versão 2 sem que ocorra um crash na versão 1. Isso acontece por que, pois mais que haja uma nova versão disponível, nada impede do cliente ainda continuar a usar a versão 1. 

O fator atualização também é muito impactante no versionamento de API's uma vez que podem existir várias versões que atendam à um momento de demanda específico do cliente para/com API. Por exemplo, a versão "A" é a que está sendo utilizada pelo cliente, a versão "B" é a versão de testes de novas features à serem implementadas à versão "A" e a versão "C" é a uma versão similar à versão "A" porém, é será utilizada pelo cliente apenas se a versão "A" estiver inutilizável, evitando interrupções do serviço. Dessa forma, torna-se perceptível o qual essencial torna-se esta metodologia para projetos mais amplos e complexos. 

#### Versionando a API pelos serialzers

Para o projeto, serão versionados especificamente outros serializers. Ou seja, haverá mais de 1 serializer atrelado à um viewset (serializerv1, serializerv2). Dessa forma, torna-se necessário definir para o viewset, qual serializer utilizar.

Para isso, será implementado o método "get_serializer_class" onde haverá um if condicional para escolher qual versão do serializer adotar. Dessa forma, a partir deste método, ele retorna uma versão do serializer.

1) Em serializers.py, crie um novo serializer respectivo à nova versão de um viewset
~~~
#serializer do estudante - versão 2    
class EstudanteSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        #note que nesta versão, existem menos campos implementados
        fields = ['id','nome','email','celular']
~~~
2) Importe os novos serializers definidos para as versões em views.py
3) Dentro da classe de viewset, implemente o método "get_serializer_class"
~~~
def get_serializer_class(self):
    #caso a versão seja a versão 1, retorne a versão 1, c.c retorne a outra versão
    if self.request.version == 'v1':
        return AccountSerializerVersion1
    return AccountSerializer
~~~
4) Lembre-se de tirar o "serializer class", pois agora o viewset selecionado pode ser definido para mais de um serializer

#### Configurando as versões da API

- Configurando o endpoint da nova versão 

O endpoint de uma API é basicamente o local que conecta a propria API com o aplicativo/cliente. Dessa forma, torna-se necessário criar um novo endpoint para a nova versão da API, assegurando que o usuário poderá acessar as duas versões por duas rotas diferentes.

Nesse sentido, será utilizado o "QueryParameterVersioning" o que será responsável por pegar o caminho da url e definir um endpoint. 

- Configurando o esquema de versionamento - Em settings.py do projeto, em REST_FRAMEWORK:
~~~
'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning'
~~~

Depois de configurado globalmente, basta apenas acessar colocando na url:
> /?version==2

# Permissões, documentação, limitações, CORS e deploy

## Limitando as requisições 
### Ordenando listas de objetos
Devido ao fato das listas de objetos não estarem ainda ordenadas. Isso pode apresentar resultados inconsistentes devido ao fato de que esse modelo não está ordenado.
Nesse sentido, ao olhar nas primeiras linhas do viewset, são definidos os queryset's (váriáveis responsáveis por capturar todas as instâncias dos modelos). Consequentemente, não basta apenas capturar as instâncias mas sim organizar elas em uma lista de objetos ordenada. Por padrão, as instâncias são organizadas por id, fora o fato de que já foi aplicado na API alguns filtros de organização. 

Contudo, da forma que atualmente está, os objetos capturados não estão sendo ordenados em seguida. Fazendo com que fique à trabalho da API cuidar desses processos de organização de listas de instâncias seja por meio do procedimento padrão ou seja por meio dos filtros já implementado. 

- Ordenando as listas de instâncias 
Em views.py, no viewset que será implementado a ordenação 
~~~
#no queryset de estudantes 
queryset = Estudante.objects.all().order_by('id')
~~~
### Limitando requisições de rota da API
Até o momento, é possível acessar as rotas da API sem nenhuma restrição pois a única condição implementada até agora é que o usuário precisa estar logado no admin. Contudo, a quantida de acessos ilimitados e irestritos podem causar problemas para o sistema, sendo completamente vulnerável à acessos em massa os quais podem causar uma sobrecarga no servidor, causando problemas de lentidão e, em casos extremos, queda do servidor. 

A depender de onde o sistema está hospedado, torna-se necessário o uso de restrições nas requisições de rota da API para evitar gastos com o serviço de hospedagem, como o esgotamento do plano ou com a chegada de custos à mais para o desenvolvimento da API.

- Throttling - Limitando as requisições globalmente
Coloque as restrições de Throttling tanto para usuários logados quanto para usuários anônimos em settings.py, REST_FRAMEWORK:
~~~
    'DEFAULT_THROTTLE_CLASSES': [
        #capturando os users anônimos pelo endereço de ip  
        'rest_framework.throttling.AnonRateThrottle',
        #capturando os users autenticado
        #onde será gerada uma chave para identificar cada user
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        #20 permissões por dia para usuários anônimos
        'anon': '20/day',
        #50 permissões por dia para usuários logados
        'user': '50/day'
    }
~~~
### Adicionando limitações personalizadas
Adicionamos a limitação por rotas de forma global. Isso significa que para qualquer rota, a quantidade de acessos que vai ser restringida será a mesma. O único parâmetro que altera isso é se o usuário está logado ou não. Surge então a necessidade de personalizar as restrições de rotas específicas. 

Para isso, o throttle aplicado dentro da configuração global será aplicado agora dentro de uma viewset específica. Por exemplo, se agora eu quiser restringir a quantidade de acessos das matrículas, terei que me atentar agora para as viewsets das matrículas.

OBS: Antes mesmo de começar os testes. Tenha certeza de que, quando for testar as limitações quando o usuário for anônimo, lembre-se de comentar/apagar momentâneamente as validações globais de que o usuário precisa estar logado para acessar a API root.

~~~
#comente tudo isso
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.IsAuthenticated',
    ],
~~~

1) Nas views.py, importe o throttle para usuário logado e anônimo 
2) Aplique o throttle na viewset específica
~~~
#crie uma classe focada na matrícula que herde a configuração global de AnonRate
class MatriculaAnonRateThrottle(AnonRateThrottle):
    #apenas troquei de 20 da config global p/ 5
    rate = '5/day'

class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all().order_by('id')
    serializer_class = MatriculaSerializer
    #aplicando o throttle na viewset de matrículas
    throttle_classes = [UserRateThrottle, MatriculaAnonRateThrottle]
~~~

Note que não há necessidade de criar uma classe especificamente para o UserRate uma vez que a quantidade de restrições da viewset será a mesma adotada na configuração global.Além disso, sempre estabeleça um número de restrições menor ou igual à da configuração global pois as restrições globais sempre terão o valor máximo.

- BOA PRÁTICA: Arquivo Throttles.py

Ao invés de adicionar um monte de classes de throttle nas views.py, em termos de organização, é mais eficiente criar um arquivo de throttles e importar os throttles de lá para os viewsets em views.py. 

1) No arquivo throttles, importe o throttle. 
2) Adicione as classes de throttles relacionadas às viewsets 
3) No arquivo de views.py, retire o import do throttle e adicione o import do arquivo throttles.py, chamando as classes do respectivo arquivo para as viewsets específicas. 

## Adicionando permissões 

### Definindo permissões por usuário
Da forma como as restrições estão implementadas, qualquer usuário logado pode acessar todas as rotas da API. Entretanto, na realidade dos projetos, cada usuário tem as próprias especifidades, as quais apontam quais rotas os users poderão acessar. 

Para este projeto, cada usuário será designado em uma função específica e as permissões sobre eles deverão ser determinadas na página de administração. De forma que todas as permissões deverão ser configuradas dentro da API. 

- Configurando os usuários 
Como a configuração será na página de administração, será um processo rápido e bem intuitivo por conta disso. Certifique-se de levar a etapa de criação da senha do usuário com mais seriedade para atender as validações pré-estabelecidas pela página de admin.

Lá você poderá acessar designar o usuário à um grupo com permissões específicas ou adiciona-las diretamente ao user 

### Adicionando permissões na API

No tópico acima, foram criados usuários e suas respectivas permissões de acesso ou CRUD na página de admin. Sendo necessário agora indicar as permissões estabelecidas no admin para cada usuário na API root.

Para fazer isso, será necessário apenas trocar as classes de permissões em settings.py. Ao invés de estabelecer o "IsAthenticated" como configuração global. Estabelecer o "DjangoModelPermissions" pois, dessa forma, o Django Rest irá basear as permissões globais nas instâncias vindas dos models, ou seja, dos usuários criados. 

### Definindo métodos http 

No projeto, as matrículas poderão ser vistas e criadas na API root utilizando os métodos GET e POST. Caso seja necessário realizar um CRUD, estas operações serão feitas na página de admin. Ou seja, a API root não pode utilizar os métodos PUT, PATCH e DELETE nas matrículas.

Dessa forma, dentro do viewset de matrículas ou qualquer viewset desejável, defina como atributos os métodos https convenientes. Dentro do viewset de matrícula, coloque:

~~~
class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all().order_by('id')
    serializer_class = MatriculaSerializer
    throttle_classes = [UserRateThrottle, MatriculaAnonRateThrottle]
    #os métodos permitidos serão apenas o GET e o POST
    http_method_names = ['get','post']
~~~

## Documentando a API
### Trabalhando com o Swagger
A medida que o projeto torna-se mais complexo, faz-se necessário registrar todas as particularidades da API, as quais podem envolver as features, restrições, validações, dentre outras operações. Nesse sentido, a documentação acaba se tornando uma forma crucial não só para a organização mas também para a continuidade do projeto, uma vez que colaboradores poderão sair e entrar no decorrer do desenvolvimento. 

Existem várias formas de documentar este projeto: pode ser por meio de um aplicativo de gerenciamento de projeto como o trello, pode ser um próprio arquivo readme.md (como esse). Além do readme.md, utilizaremos para este projeto o swagger|OpenAPI 2 com os estilos de documentação swagger UI e redoc.

O swagger é uma estrutura de software pronta para a documentação, consumo e criação de APIs. Para este projeto, o swagger será utilizado apenas para a documentação. O OpenAPI 2 tratasse de uma especificação pronta para indicar os pontos que devem ser estruturados na documentação da API, escrevendo os dados de forma organizada e detalhada.

1) Instale os pacotes de suporte do swagger e do OpenAPI 2: drf-yasg
> pip install drf-yasg
obs: lembre-se de atualizar o requirements.txt 
> pip freeze > requirements.txt
2) Configure os pacotes no settings.py, em INSTALLED_APPS
~~~
'drf_yasg'
~~~

### Configurando o Swagger
- Configurando a url 
Em urls.py, será criado um schema_view o qual irá conter todas as informações que precisa passar para a documentação: título, versão, descrição, termos de serviço, contato, licença, se é pública ou privada, permissões, etc. 

1) Em urls.py importe do pacote de yasg o get_schema_view e o opeapi
2) Implemente a classe schema_view
~~~
schema_view = get_schema_view(
   openapi.Info(
      title="Documentação da API",
      default_version='v1',
      description="Documentação da API Escola",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)
~~~
3) Configure os estilos de documentação em urlpatterns 
~~~
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
~~~

Dessa forma, será possível acessar a view do swagger acessando o "endereçoroot/swagger". Onde, de acordo com o usuário logado, será possível ter acesso aos métodos http referentes a cada model. Além de, claro, ter acesso à uma documentação geral da API.

É possível implementar uma documentação diretamente em funções, métodos e classes por meio de docstrings. Os quais servem saber para que serve aquele bloco, qual a função ele exerce e o que ele retorna. Por exemplo: 

~~~
class ListaMatriculaEstudante(generics.ListAPIView):
    #isso é uma docstring
    """
    Descrição da View:
    - Lista Matriculas por id de Estudante
    Parâmetros:
    - pk (int): O identificador primário do objeto. Deve ser um número inteiro.
    """
    def get_queryset(self):
        queryset = Matricula.objects.filter(estudante_id = self.kwargs['pk']).order_by('id')
        return queryset
    serializer_class = ListaMatriculasEstudanteSerializer
~~~

### Verificando o Redoc
O redoc proporcionará uma interface adaptada e pronta para a visualização da documentação da API, permitindo uma melhor visualização da desde da documentação geral até das docstrings implementadas nas viewsets, por exemplo. 

## Integrando a API com o front end 
### Preparando o ambiente
Para executar o projeto, será necessário utilizar o docker na sua máquina. O docker é uma plataforma open source que permite desenvolver, criar e executar arquivos dentro de contêines. 

Vale salientar primeiramente que o projeto front end que utilizei foi o mesmo ofertado pela Alura durante o curso.

- Analisando o projeto front end 

A primeira coisa à ser analisada lá é entender o que é o "dockerfile". O "dockerfile" será responsável por criar uma imagem do docker, a qual irá conter todas as informações de como a aplicação front-end será executada.

O docker-compose é responsável por rodar o conteiner do docker, contendo todas as informações de serviços que serão utilizados. O docker-compose será responsável por rodar o conteiner do docker e subir o servidor do front-end e mantê-lo no ar.
 
Nesse sentido, existem alguns detalhes relevantes para o projeto da API que devem ser levados em consideração.

Em docker-compose.yaml
~~~
version: '3.8'
services:
  nginx:
    build:
      context: . 
      dockerfile: Dockerfile 
      args:
      #Contém o ambiente para carregar as informações
        - VITE_URL=${VITE_URL}
    #A porta que o servidor irá subir -> localhost 8042
    ports:
      - "8042:80" 
    command: ["/bin/sh", "-c", "nginx -g 'daemon off;'"]
~~~

Note que em ".env" haverá um "VITE_URL". Esse link irá proporcionar um arquivo Json capturado da API root por meio do método GET. Vale mencionar que este arquivo Json tratasse de um arquivo fixo, pois se compararmos com os Json's capturados da API root, é possível detectar que os Id's do Json capturado em "VITE_URL" não tem uma ordem específica e são todos definidos como 0.

- OBS: Instale o WSL (Windows Subsystem for Linux) [OPÇÃO WINDOWS]

O WSL é um subsistema Linux feito para ser executado dentro do Windows. Caso o sistema operacional utilizado seja Windows, torna-se necessário instalar o WSL por que ele permite ao usuário executar um ambiente Linux diretamente no Windows, sem a necessidade de usar uma máquina virtual ou realizar um dual boot. Como o Docker é mais otimizado para Linux, o software acaba sendo executado de forma mais rápida e otimizada.

### Subindo o container do front end
Com a pasta aberta onde está o conteúdo que será "conteinerzado", abra um terminal WSL (ubuntu) e, em seguida: 

>docker-compose up --build

Dessa forma, o docker irá fazer a construção da imagem do conteiner, ou seja, ele irá criar um arquivo executável que contém todos os arquivos, módulos, bibliotecas e dependências necessárias para executar o conteiner.

Logo após esta etapa, no aplicativo de desktop do docker, é possível acessar os conteiners e as imagens criadas.

- Alterando projetos "conteinerzados"

Toda vez que o conteiner seja aberto, o servidor do mesmo também abre. Dessa forma, caso seja necessário realizar alterações do projeto no projeto, o recomendável é excluir a imagem anterior para evitar que haja conflito com informações anteriores do projeto.  

### Acessando o projeto front-end
Como visto acima, no arquivo "docker-compose.yaml" é possível pegar a porta do conteiner que foi subido para acessar a parte front-end, basta apenas inserir a seguinte url:

> localhost:8042

### Integrando o front-end com o back-end

Da forma como atualmente está, os dados exibidos no projeto front-end contém apenas informações fixas captadas por um método GET feito anteriormente. Isso é definitivamente um problema pois toda vez que os dados dos cursos, estudantes e matriculas forem alteradas, os dados capturados no front-end permanecerão inauterados e incorretos.  

Com isso, faz-se necessário integrar o front-end com os dados atualizados do back-end. 

1) Caso esteja ligado, pare o servidor do conteiner para realizer as alterações.

2) No projeto front-end, em ".env", "VITE_URL" passe o path referente à parte do back-end que você quer integrar. No caso do projeto, foi passado o localhost da API root, especificamente do endpoint de cursos.

3) Antes de subir o container/servidor, no app de desktop do docker, apague a imagem anterior e inicie o conteiner. 

4) Suba o container alterado 
> docker-compose up --build

- Caso esteja subindo um container com alterações 

> docker-compose up --build

- Caso esteja subindo um conteiner sem alterações

> docker-compose up

### Entendendo o CORS

Ao verificar se o front-end atualizou, foi dado como se não tivesse cursos listados. E ao clicar em especionar a página, foi detectado uma falha em acessar o path de cursos pois teve um bloqueio pela política do CORS, especificamente por não ter nenhum acesso "control-allow-origin" presente no projeto.

- O que é CORS 

É basicamente um mecanismo que gerencia a comunicação entre cliente e servidor e checa se tem ou não a permissão de autorizar a comunicação entre os dois. O CORS é aplicado na comunicação entre domínios diferentes e, como estamos relacionando o localhost de cursos com o localhost da aplicação do front-end

### Configurando o CORS

Será importante configurar o CORS uma vez que precisa-se, de alguma forma, indicar que os recursos do domínio do backend (especificamente, da API) podem ser consumidos pelo domínio do front-end.

Para resolver este problema, utilizaremos a biblioteca django-cors-headers. O intuito de utilizar ela será para criar cabecalhos para indicar certas informações. Especificamente, serão atribuidas aos headers informações de validação, como permitir ou negar recursos e acessos à dominios diferentes. 

1) Instale a biblioteca django-cors-headers 
> pip install django-cors-headers

2) Em settings.py, em INSTALLED_APPS, adicione:
~~~
INSTALLED_APPS = [ 
    ...
    'corsheaders',
]
~~~
3) Ainda em settings.py, em MIDDLEWARE, adicione: 

~~~
INSTALLED_APPS = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
~~~

Lembre-se de colocar este middleware acima dos outros middlewares (especificamente, acima do "commom middleware") tendo em vista que o "corsheaders" é um middleware de resposta.

4) Defina as origens que serão acessadas no final de settings.py

~~~
CORS_ALLOWED_ORIGINS = [
    #origin do front-end
    "http://localhost:8042",
    "http://127.0.0.1:8042",
]
~~~

OBS1: Existem outras formas de definir as origens além de atribuir uma lista de autorização específica para elas, como permitir uma lista de origens tendo como base regex ou permitir todas as origens ou nenhuma por meio de um booleano.

- Autenticando as rotas     

Com o CORS estabelecido, a API está sendo autenticada, logo, será necessário passar por uma etapa de autenticação para qualquer rota que seja acessada. Daí temos o seguinte problema: o front-end por si só não conseguirá interpretar essa situação e passar a informação de autenticação de acordo com o que foi feito na interface do sistema.

Consequentemente, não será possível manter a autenticação do "DjangoModelsPermissions" (por tabela, o "is_authenticated" também). Ou seja, nas rotas da API as quais estão sendo integradas no front-end, precisará de um novo tipo de autenticação.

O objetivo é fazer com que após a autenticação para uma certa rota (por exemplo a de cursos), o front-end consiga apenas ler as informações da rota e, como o front-end precisa apenas acessar rotas específicas, não há necessidade alguma de aplicar a autenticação de forma global.

Em views.py, adicione uma autenticação específica para a rota de cursos

1) Importe IsAuthenticatedOrReadOnly 
2) Aplique esta autenticação para dentro da classe viewset de cursos
~~~
permission_classes = [IsAuthenticatedOrReadOnly]
~~~

OBS: Lembre-se de subir o conteiner do front-end toda vez que for testar a API, uma vez que agora, o API root e o front-end estarão integrados, de forma que o front-end realiza requisições para a rota de cursos da API, processa os dados e os apresenta de forma mais organizada e clara para o usuário.

## Realizando deploy

- O que é deploy 

Tendo em vista todos os processos feitos para a implementação desta API como criação, validações, permissões, buscas, filtros e documentação, a próxima etapa do desenvolvimento da API será a etapa de deploy. 

A etapa de deploy consiste basicamente em colocar a aplicação no ar, para que seja executada em outros locais além da sua própria máquina, disponibilizando a aplicação para uso, seja de um ambiente de desenvolvimento, teste ou produção. Nesse sentido, tal etapa faz se necessária justamente por que os usuários finais da aplicação: os clientes, não conseguiriam acessar a aplicação pelo fato dela estar disponível apenas em local host. 

Esta etapa é importante para o desenvolvimento de qualquer aplicação pois serve como uma simulação de como ela se comportaria na prática. É a partir dela que é possível diagnosticar o status da aplicação para saber quais são os seus erros e, dessa forma, planejar as proximas manutenções do sistema, tal como a implementação de novas features. 

### Preparando o ambiente
Para este projeto, a etapa de deploy será implementada na AWS (Amazon Web Services) com o intuito de automatizar a implantação do projeto no serviço de computação em nuvem de lá, aproveitando a escalabilidade e a confiabilidade da infraestrutura de nuvem da Amazon.

Primeiramente, é necessário configurar e preparar a API para o processo de deploy, 

1) Coloque o projeto construído em um repositório do github (como esse, por exemplo)
2) Dentro do repositório, crie uma nova branch para o deploy
3) Dentro da branch de deploy, em settings.py do setup:
~~~
ALLOWED_HOSTS = ['*']
~~~
Isso irá fazer com que todos os hosts (servidores) sejam permitidos para o projeto, autorizando o uso da aplicação em um desses serviços de computação. 

### Configurando projeto e criando uma instância AWS 

Agora na AWS, será necessário criar um ambiente de produção para a API.

Especificamente para este projeto, será utilizado o Amazon EC2 para hospedar a API, o qual é um serviço que fornece capacidade de computação redimensionável na nuvem da Amazon

Dentro da AWS:

> ECS > executar/criar instâncias
> AMI (imagem de máquina da amazon) escolhida foi ubuntu
> serviço de instância utilizada: ts.micro
> ATENÇÃO: baixe e guarde os pares de chave para se logar na instância

No final, a instância estará criada com o status de "executando"

### Fazendo deploy na AWS 

1) Acesse a instância criada pelo id 
2) Conecte-se com a máquina virtual 
3) Dentro do terminal da máquina (vai depender do sistema operacional que você optou):
    - Atualize o terminal 
    > sudo apt update
    - Verifique a versão do python 
    > python3 --version
    - Copie o endereço do seu repositório e faça um git clone na máquina virtual
    > git clone "link do repositório"
    Obs: lembre-se de gerar um token para utilizá-lo como autenticação na máquina virtual
    - Verifique a branch atual e mude para a branch de deploy 
    > git branch 
    > git checkout deploy

4) Instale, crie e ative um ambiente virtual na máquina virtual

Dentro do repositório clonado, instale o ambiente virtual
> sudo apt install python3.12-venv

Crie o ambiente virutal
> python3 -m venv venv

Ative o ambiente virtual criado 
> source venv/bin/activate

Obs: Uma vez criado o ambiente virtual, só precisará ativá-lo na próxima vez.

5) Dentro do ambiente virtual, instale as dependências do projeto, faça as migrações, crie um superusuário 
> pip install -r requirements.txt
> python manage.py makemigrations
> python manage.py migrate 
> python manage.py createsuperuser

Obs: caso não consiga instalar corretamente de primeira, tente primeiramente instalar este kit de ferramentas:

> pip install setuptools

6) Configure a porta 

Diferentemente do que estava sendo aplicado no ambiente de desenvolvimento com localhost, agora será necessário definir uma porta para subir o servidor. A configuração desta porta será feita manualmente na AWS em: Instância > Segurança > Grupos de Segurança > Regras de entrada (editar regras de entrada).

Adicione uma nova regra: TCP personalizada, intervalo de portas 8000, bloco CIDR 0.0.0.0/0

7) Suba o servidor

> python manage.py runserver (porta adicionada: 0.0.0.0:8000)

Para conferir se está funcionando, em outra aba, coloque na URL:
> (Ip público):8000

8) Popule o banco de dados (opcional)

Caso os dados do banco de dados não seja importado para a máquina virtual, popule novamente os bancos de dados com: 

> python3 popular_banco_cursos.py
> python3 popular_banco_estudantes.py

### Trabalhando em segundo plano 

Da forma como a instância está sendo utilizida, ela está fazendo a mesma coisa que a máquina local faria: rodar a aplicação de forma local. Ou seja, se a instância criada for fechada, a aplicação é fechada também. Desta forma, faz-se necessário configurar o servidor para que a instância criada consiga operar em segundo plano em:  id da instâncias > conectar instânicas. Dentro da máquina virtual:

1) Verifique as aplicações que estão rodando em segundo plano
> screen -list
2) Determine que a aplicação rodando está em segundo plano 
> screen -S (nome da pasta, nesse caso, a mesma clonada do git)

Caso queira confirmar, utilize o comando do passo 1 para verificar se a aplicação está na lista de screen. Além disso, logo após subir o servidor da API, independentemente da aba da instância estiver aberta ou fechada, a API continuará ativa. 

- Parando instâncias 

É possível parar a execução das instâncias, podendo interromper ou encerrar. Isso é importante pois como a instância que está sendo aplicada para a hospedagem do projeto é paga, é preciso ficar de olho no tempo em que a instância está sendo executada. Sendo necessário interromper o processo quando não estiver utilizando para evitar a vinda gastos não planejados.

# Trabalhando com testes unitários e de integração 

Os testes unitários e de integração são dois tipos de níveis de teste diferentes mas ambos compartilham um mesmo objetivo final: garantir com que o projeto que está sendo testado atenda todas as necessidades do utilizador final. Ou seja, quanto mais abrangentes e diversificados forem o conjunto de testes utilizados, maior será a qualidade, eficiência e confiabilidade do produto a ser entregue. 

Existem vários níveis de testes como de aceitação do usuário, regressão, desempenho, segurança, etc. Para este projeto, serão aplicados apenas alguns testes unitários e de integração. 

## Conhecendo os tipos de testes

- Testes unitários

São basicamente pequenos trechos de códigos ou scripts escritos individuais para verificar a confiabilidade de alguma parte específica de código do projeto como uma função ou um método. Isso serve para verificar se aquele trecho do código fonte está se comportando como deveria ou não.  

Estes tipos de testes são projetados para isolar e testar um unidade de código de maneira independente ao resto do projeto. Geralmente eles são responsáveis por identificar error e bugs de locais específicos a fim de evitar que tal erro escalone mais ainda para o resto da aplicação. Sendo considerados mais rápidos de desenvolver e executar, com um custo de produção menor. 

- Testes de integração 

Uma vez que temos partes específicas do código verificadas por meio de testes unitários, faz-se necessária a utilização de testes de integração para verificar se à algum erro na conexão entre os trechos de códigos verificados. 

Nesse sentido, estes tipos de testes tem como objetivo identificar e solucionar problemas de interface e interoperabilidade tal como realizar o compartilhamento correto de dados entre os componentes.

- End to end (de ponta à ponta)

Testes que verificam o fluxo do sistema por completo, simulando os resultados finais. São os testes mais próximos de ambiente de produção, simulando tal ambiente. Por se um teste mais avançado e que possui um sistema praticamente pronto, ele é um teste que apresenta um custo mais elevado, com um tempo maior para desenvolve-lo.

Dessa forma, é possível interder os tipos de testes em diferentes níveis, como se fosse uma pirâmide onde a base são os testes unitários, os quais servem como base para os testes de integração, que por sua vez, são como base para os testes "end to end".

![piramide_de_testes](/readme_assets/piramide_de_testes.jpg)

Note que, quanto mais próximo o tipo de teste se aproxima do topo, mais caro e mais complexo ele se torna. Tal como a quantidade de testes, que se relaciona de forma inversa à piramide.

### Tipos de testes

- Testes manuais

São testes os quais são executados por quem está planejando o projeto de forma manualmente. Ou seja, são testes impostos pelos programadores onde eles se põe em uma situação específica para caso o usuário digite um dado errado do formulário.

Podemos citar como exemplo de teste manual o teste de verificação do cpf. Para realmente testar esse campo do formulário atualmente, o programador propositalmente preenche o campo de forma errada para conferir de forma manual se a aplicação irá detectar o erro ou não. 

Contudo, além deste trabalho ser bastante massante e repetitivo, pelo fato do ser humano ser limitado por natureza, é inevitável a presença de falhas e bugs nestes testes.  Pois estes testes deverão ser verificados e conferidos todas as vezes em que forem executados. 

- Testes automatizados

Testes feitos pela máquina. Basicamente, são testes feitos por softwares os quais possuem scripts pré-determinados os quais nos permitem indicar os cenários de testes que devem ser realizados. Pelo fato de ser um script "pronto", você pode aplicá-lo várias vezes para testar vários cenários com mais eficiência e velocidade do que a forma manual. 

### Testando a API no ThunderClient

O ThunderClient é uma extensão do vscode a qual será utilizada para testar a API REST do projeto. Ela irá, especificamente, para testar as requisições. Foi utilizado nesse projeto para ter uma melhor visão de como uma única requisição recebe vários testes e como cada um deles se relacionam. 

Para titulo de exemplo, foi utilizada a requisição GET da rota de estudantes: 
> http://127.0.0.1:8000/estudantes/

Quando a requisição GET for checada após ser enviada, ela terá como status code: "401 Unauthorized". Isso poderá ser solicionado indo para a aba de testes, selecionando um novo teste do tipo "code response" igual ao 401, que é o código do status. Ao enviar novamente a requisição, bastou apenas conferir na aba de resultados de testes de que o resultado passou e estava ok. 

- Testando se o código de resposta está correto

A questão é que no cenário em que esta requisição está sendo testada, a API precisa ser autenticada. Logo, faz-se necessário realizar a autenticação de um super usuário por exemplo. Consequentemente, o status irá se alterar para "200 ok", fazendo com que o teste seja alterado de "401" para "200".

- Testando se o corpo da resposta é Json 

Para implementar este teste basta apenas adicionar um novo teste com "responsebody isjson"

- Testando o tipo de conteúdo da resposta 

De forma paralela aos demais: "conten-type equal application/json"

- Testes e scripts 

Os testes que serão implementados no cenário que foi montado devem englobar não só aqueles que dão certo, mas também aqueles que dão erro. Dessa forma, aquele "responsecode equal 401" deveria também ser implementado. Note que, dependendo da condição: o usuário está autenticado ou não, o status receberar um resultado diferente, sendo hora 401, hora 200.

Dessa forma, faz-se necessária a implementação de scripts de testes para melhor organizar a forma como é testada a requisição GET dos estudantes. Contudo, de acordo com a documentação do thunderclient, a linguagem utilizada para escrever esses scripts é javascript.

Nesse sentido, por motivo do foco do projeto ser relacionado à linguagem python, os testes serão desenvolvidos em outro local sem ser o ThunderClient.

- Boa prática: Pasta "tests"

A fim de criar vários cenários de testes para várias possibilidades, torna-se mais viável criar uma nova pasta dentro da aplicação. É nela onde os arquivos de script para teste serão desenvolvidos. 

1) Crie uma pasta "tests" dentro do app a ser testado (nesse caso aqui: escola)
2) Dentro da pasta, informe à pasta que ela é um módulo do python criando um arquivo "__ init_ _.py" 
3) Para evitar futuros conflitos, dele o arquivo tests.py 

## Testes de model e serializer

### Trabalhando com teste unitário em Django

Foi utilizado o módulo de "testecase" para a criação dos testes unitários. Independentemente se o teste fosse aplicado sobre um modelo ou sobre um serializador. 

- Exemplificando um teste qualquer 

1) Crie um novo arquivo na pastas "tests", chamado "test_models.py", feito para os testes para as models do projeto. 
2) Importe a biblioteca de testes do django e os modelos à serem testados.
3) Crie uma classe de teste para um respectivo modelo, onde os métodos de tal classe serão justamente os métodos que serão utilizados para realizar os testes naquele módulo.
~~~
class Model<nome_da_model>TestCase(TestCase):
    def <teste_específico_x> (self): 
        ...
~~~ 

- Identificando se o teste funcionou

À título de exemplo, foi criado um método de testmodel que sempre falha. Para verificar se o teste funcionou ou não, faça o seguinte no terminal: 

> python manage.py test

Esse comando irá apontar quais testes passaram (.) e quais testes falharam (F).

### Testando um model 

Crie os testes dos modelos no arquivo "test_models.py".

1) Crie a classe de teste do modelo:
2) Dentro da classe, crie uma função de setup, a qual servirar para preparar o ambiente de testes. 

Para este projeto, o cenário de testes precisa contemplar testes referentes aos atributos do modelo de estudante: nome, email, cpf, etc.

~~~
class ModelEstudanteTestCase(TestCase):
    # criando o ambiente de testes 
    def setUp(self):
        #criando um objeto baseado no modelo estudante -> criando um estudante-teste
        self.estudante = Estudante.objects.create(
            #atributos vindos do modelo estudante
            nome = 'Teste de modelo',
            email = 'testedemodelo@gmail.com',
            cpf = '95197262095',
            data_nascimento = '2023-02-02',
            celular = '84 99999-9999'
        )
~~~

Vale salientar que, para a realização dos testes, será criado um banco de dados próprio para que as informações do banco de dados da aplicação não sejam alteradas durante a execução dos testes. 

3) Uma vez criado o setup para a model de estudante, crie o método específico. Para o projeto, será um teste para verificar se os atributos corretos.

~~~
    def test_verifica_atributos_de_estudantes(self):
        #documentando de forma isolada com a docstring
        '''Teste que verifica os atributos do modelo de estudante'''
        #comparando valores armazenados com os valores à serem criados como exemplo acima
        self.assertEqual(self.estudante.nome, 'Teste de Modelo')
        self.assertEqual(self.estudante.email, 'testedemodelo@gmail.com')
        self.assertEqual(self.estudante.cpf, '95197262095')
        self.assertEqual(self.estudante.data_nascimento, '2023-02-02')
        self.assertEqual(self.estudante.celular, '84 99999-9999')
~~~

Vale mencionar que foram realizados testes do mesmo tipo para os modelos de curso e matrícula.

### Testando um serializer

O intuito dos testes nos serializers será para verificar os campos que estão sendo serializados tal como os conteúdos relacionados a cada campo. 

1) Crie um arquivo de testes para serializers: "test_serializers.py".
2) Dentro de "test_serializers.py", importe o módulo de testes do django, juntamente com os serializers a serem testados e seus respectivos modelos.
3) Crie uma classe para os testes do serializer baseado na model estudante e, dentro dela, crie a função de setup:
~~~
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
~~~

4) Aplique os testes. Para o projeto, serão aplicados os dois testes já mencionados acima: 

~~~
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
~~~

Vale mencionar que foram realizados testes do mesmo tipo para os serializers de curso e matrícula.

## Testes de autenticação 

Agora será necessário aplicar testes de aplicação, para evitar de acontecer o que ocorreu no exemplo envolvendo o thunderclient, onde a depender do estado de autenticação do usuário (estar logado ou não) o "responsecode" mudava. Ou seja, sempre que tentava-se testar os dois cenários (usuário logado ou deslogado), estava dando conflito. Nesse sentido, o teste de autenticação será feito tendo como base a criação de um script, de modo que seja possível testar os cenários simultaneamente.

Para o projeto, serão realizados testes de autenticação do usuário com as credenciais corretas e incorretas, por meio do "username" e da senha. Também serão realizados testes de autenticação referentes à requisições GET autorizadas e não autorizadas para a rota de estudantes. 

### Criando testes de autenticação

Os testes criados abaixo são considerados como testes unitários pois o seu respectivo cenário de testes contempla apenas uma parte isolada do código, especificamente, referente apenas à autenticação do usuário.   

1) Dentro da pasta de testes, crie um arquivo de teste de autenticação: "test_authentication.py".

2) Importe os models de autenticação, o "testcase" para a API e o "authenticate"

3) Crie um classe para a autenticação do usuário juntamente com o "setUp", responsável por configurar o ambiente de testes para tal autenticação e onde será criado um superusuário que será utilizado para os testes de autenticação.

4) Crie os testes. (Os testes a serem criados para o projeto, já foram mencionados no começo do tópico)

Procedimento similar aos outros testes: o teste será basicamente um método dentro da classe de autenticação do usuário. Estes que, por sua vez, poderão ser documentados por meio de docstrings. Como exemplo, eis aqui um dos: 

~~~
    def test_autenticacao_user_com_credenciais_corretas(self):
        '''Teste que verifica a autenticação de um user com as credenciais corretas'''
        #autenticando o usuário 
        usuario = authenticate(username= 'admin', password= 'admin')
        #verificando se a autenticação deu certo ou não:
        #o dado não pode ser vazio e o no usuário será aplicada a condição de autenticado
        self.assertTrue((usuario is not None) and usuario.is_authenticated) 
~~~

5) Confira os testes utilizando: 
> python manage.py test 

### Testes de autenticação na requisição GET 

A abordagem para aplicar os testes de requisição será um pouco diferente pelo fato de que agora, estes testes envolverão dois ou mais pontos do sistema à serem integrados, sendo agora necessário utilizar testes de integração.

Como agora, as requisições GET para estudantes precisam ser testadas, é preciso capturar a url de estudantes. Isso acontecerá utilizando o "basename" de tal url da seguinte forma.

1) Importe do "django urls" o "reverse", e do "drf", o "status".

2) Adicione na função de setup a url, capturando os dados dela.

~~~
self.url = reverse('<basename_de_estudantes>-list')
~~~

Obs: o "-list" serve para capturar a rota que faz lista todas as informações dos estudantes. Ou seja, a url de estudante que está sendo capturada é capaz apenas de ler/listar as informações contidas nela. 

3) Crie o teste para fazer a requisição da url.
~~~
    def test_requisicao_get_autorizada(self):
        '''Teste que verifica uma requisição GET autorizada'''
        #a rota "url" precisa ser autenticada... forçando a autenticação abaixo
        self.client.force_authenticate(self.usuario)
        #capturando uma variável "response" e simulando a requisição
        response = self.client.get(self.url)
        #comparando o número da response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
~~~ 

### Autenticando os testes de rotas 

Antes de implementar os testes de API, partir do pressuposto de que todas as rotas já estão autenticadas, para isso:

1) Dentro da pasta de testes, crie um arquivo de testes para cada rota.

Os próximos passos serão feitos tendo como base o ambiente de testes para a rota de estudantes. A aplicação dos testes nas demais rotas foi feita de forma análoga.

2) Importe as bibliotecas necessárias: User, APITestCase, reverse e status
3) Crie a classe de casos de teste (testcase) para a rota de estudantes, juntamente com o ambiente de testes definido por setUp.

~~~
class EstudantesTestCase(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_superuser(username='admin', password= 'admin')
        self.url = reverse('Estudantes-list')
        #force a autenticação já no ambiente de teste definido por "setUp"
        self.client.force_authenticate(user= self.usuario)
~~~

Tendo os ambientes para testes autenticados, agora serão realizados os testes de requisição get, post, put e delete.

## Testes de requisição 

Agora serão implementados os testes da API, referentes as rotas de estudantes, cursos e matrículas. Onde em cada uma dessas rotas, serão testadas as requisições get, post, put e delete. Não estamos mais trabalhando com testes de autenticação e, por conta disso, a requisição precisava ser autorizada.

Vale salientar que estes testes também foram implementados para as rotas de cursos e matriculas. 

### Testando requisição GET

A título de exemplo, o passo à passo fará os testes aplicados especificamente às requisições referentes a rota de estudantes.

1) Crie objetos de estudantes baseados no seu respectivo modelo para aplicar nos testes

Para isso, importe a model de estudante e prepare o ambiente de testes (setup) criando lá 2 estudantes:

~~~
        #exemplo = criando estudante 01 
        self.estudante_01 = Estudante.objects.create(
            nome = 'Teste estudante UM',
            email = 'testeestudante01@gmail.com',
            cpf = '33989124005',
            data_nascimento = '2024-01-02',
            celular = '84 99999-9999',
        )
~~~

2) Crie o teste 

Para o projeto, foi criado um teste de requisição get para listar os estudantes

~~~
    def test_requisicao_get_para_listar_estudantes(self):
        '''Teste de requisição GET'''
        #puxe o código de response para capturar a informação dos estudantes do GET    
        response = self.client.get(self.url) #(/estudantes/)
        #comparando o statuscode recebido do teste
        self.assertEqual(response.status_code,status.HTTP_200_OK)
~~~

Obs: Esta requisição lista todos os estudantes

3) Verifique se o teste foi bem sucedido utilizando: 

> python manage.py test 

### Testando requisição POST

~~~
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
~~~

Os testes de requisições são bastantes similares uns com os outros. Nesse caso, o "response" irá receber um método post o qual irá pegar a base de dados necessárias para criar um estudante. Dessa forma, um conjunto de dados fictícios para testes foi criado para implementar o teste. Outra mudança foi referente à comparação do codigo "response" o qual agora é comparado com o status code http 201.

Para o caso da matrícula, será necessário capturar tanto o estudante quanto o curso para criar a matricula por meio da "primary key" (pk), a qual representa o id respectivo do estudante e do curso.

### Testando requisição PUT
~~~
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
~~~

Dada uma instância já existente, compare o "status code" do response associado à requisição PUT feita ao código response OK.

### Testando requisição DELETE
~~~
    def test_requisicao_delete_um_estudante(self):
        """Teste de requisição DELETE um estudante"""
        response = self.client.delete(f'{self.url}2/')#/estudantes/2/ que eu quero deletar
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
~~~

Para testar se estava deletando a instância, escolhi a instância de estudante_2 para ser deletada. Para o teste da requisição da matrícula, será necessário trocar a comparação do status code para 405.

## Trabalhando com Fixtures 

Durante a criação e aplicação dos testes para o projeto, foram utilizados dados fictícios criados para os diversos cenários de testes. Dependendo da escalabilidade do projeto, os testes ficarão cada vez mais extensos e maçantes de serem escritos e, além disso, haverão cenários em que os dados a serem testados precisam ser os mais condizentes possível com relação aos dados reais. 

Nesse sentido serão utilizados fixtures para capturar as informações do banco de dados e passar pro ambiente de teste sem afetar a aplicação pois estes arquivos armazenam os conteúdos serializados do banco de dados da aplicação. 

- dumpdata


Este comando será responsável por capturar a colação de dados do banco de dados da aplicação e serializar eles para um arquivo de formato escolhido (um arquivo json, por exemplo). Este arquivo é chamado de Fixture. 

- loaddata
> python manage.py loaddata

Faz o processo oposto. Os dados presentes em uma certa Fixture serão implementados no banco de dados do projeto. 

### Testando Fixtures: Dumpdata e Carregando Fixtures 

- Usando o dumpdata

> python manage.py dumpdata > prototipo_banco.json

Criará um arquivo com os dados (nesse caso, no formato json) que servirá como um protótipo do banco de dados original. Lembre-se de formatar o documento.

Nesse documento, pode-se encontrar informações referentes aos estudantes, cursos, matrículas e até mesmos os usuários cadastrados na aplicação. Dessa forma, é possível coletar estes dados e aplicar nos testes já construídos. 

- Carregando as fixtures 

1) Importe o testcase para criar o ambiente de testes e as models de estudante e curso para capturar as informações.

2) Crie a classe de testcase e, dentro dela, carregue o arquivo de fixtures:
~~~
class FixturesTestCase(TestCase):
    #carregando o arquivo fixture
    fixtures = ['escola/fixtures/prototipo_banco.json']
~~~

Vale salientar que, para deixar mais organizado, criei uma pasta dedicada às fixtures.

3) Crie o método/teste para carregar as fixtures
~~~
    def test_carregamento_da_fixtures(self):
        '''Teste que verifica o carregamento da fixtures'''
        #capturando as informações da fixtures -> ex: cpf da estudante Lorena Martins
        estudante = Estudante.objects.get(cpf='66196939033')
        #capturando as informações da fixtures -> ex: código do curso "como ganhar dinheiro"
        curso = Curso.objects.get(pk=1) 
        #conferindo celular do estudante
        self.assertEqual(estudante.celular, '13 99247-9220') 
        #conferindo o código do curso
        self.assertEqual(curso.codigo,'como ganhar dinheiro') 
~~~

4) Confira se está tudo ok aplicando: 
> python manage.py test

Obs: Lembre-se que a fixture criada precisa ter sua codificação em utf-8

### Adicionando Fixtures nos testes 

Nesse momento em diante, ao invés de criar uma instância-teste de estudante/curso/matrícula, basta apenas utilizar os dados oriundos da fixture criada. 

Para o exemplo abaixo, adicionei as fixtures nos testes de estudantes mas voltou a dizer que elas serão implementadas nos cursos e nas matrículas. 

1) No começo da classe de testcase, capture o banco de dados inserido na variável de feature.  
~~~
class EstudantesTestCase(APITestCase):
    fixtures = ['escola/fixtures/prototipo_banco.json']
~~~
2) Ao invés de criar o superusuário, capture um já existente por meio de um get 
~~~
        #self.usuario = User.objects.create_superuser(username='admin', password= 'admin')
        self.usuario = User.objects.get(username= 'gui') #ATUAL 
~~~
3) Ao invés de criar os estudantes-teste, capture um já existente por meio das primary-keys.
~~~
        #criando estudante 01 
        #self.estudante_01 = Estudante.objects.create(
            #nome = 'Teste estudante UM',
            #email = 'testeestudante01@gmail.com',
            #cpf = '33989124005',
            #data_nascimento = '2024-01-02',
            #celular = '84 99999-9999'
        #)
        self.estudante_01 = Estudante.objects.get(pk=1) #ATUAL
~~~
