from django.contrib.auth.models import User

from portfolio.models import Projeto, Tecnologia


def create_user(username='usuario', password='senha12345', **kwargs):
    defaults = {
        'first_name': 'Usuario',
        'email': f'{username}@example.com',
    }
    defaults.update(kwargs)
    return User.objects.create_user(
        username=username,
        password=password,
        **defaults,
    )


def projeto_post_data(**overrides):
    data = {
        'titulo': 'Projeto Django',
        'descricao': 'Descrição com mais de dez caracteres para validação.',
        'disciplina': 'Programação Web I',
        'semestre': '2026.1',
        'status': 'em_andamento',
        'repositorio': 'https://github.com/exemplo/projeto',
        'integrantes': 'Ana Silva, João Santos',
        'tecnologias': 'Python, Django',
    }
    data.update(overrides)
    return data


def registro_post_data(username='novo_user', email='novo@example.com', **overrides):
    data = {
        'first_name': 'Novo Usuario',
        'username': username,
        'email': email,
        'password1': 'SenhaForte123!',
        'password2': 'SenhaForte123!',
    }
    data.update(overrides)
    return data


def create_projeto(autor, titulo='Projeto Teste', **kwargs):
    tecnologia_nomes = kwargs.pop('tecnologia_nomes', ['Python'])
    projeto = Projeto.objects.create(
        autor=autor,
        titulo=titulo,
        descricao=kwargs.pop(
            'descricao',
            'Descrição com mais de dez caracteres para validação.',
        ),
        disciplina=kwargs.pop('disciplina', 'Programação Web I'),
        semestre=kwargs.pop('semestre', '2026.1'),
        status=kwargs.pop('status', 'em_andamento'),
        repositorio=kwargs.pop('repositorio', 'https://github.com/exemplo/projeto'),
        integrantes=kwargs.pop('integrantes', 'Integrante Um'),
        **kwargs,
    )
    for nome in tecnologia_nomes:
        tecnologia, _ = Tecnologia.objects.get_or_create(nome=nome)
        projeto.tecnologias.add(tecnologia)
    return projeto
