from django.test import TestCase

from portfolio.models import Projeto, Tecnologia
from portfolio.tests.base import create_projeto, create_user


class PortfolioModelTests(TestCase):
    def setUp(self):
        self.user = create_user('autor')

    def test_tecnologia_str(self):
        tecnologia = Tecnologia.objects.create(nome='Django')
        self.assertEqual(str(tecnologia), 'Django')

    def test_projeto_str(self):
        projeto = create_projeto(self.user, titulo='Meu Projeto')
        self.assertEqual(str(projeto), 'Meu Projeto')

    def test_projeto_criacao_completa(self):
        projeto = create_projeto(
            self.user,
            titulo='Projeto Completo',
            tecnologia_nomes=['Python', 'Django'],
        )
        self.assertEqual(projeto.autor, self.user)
        self.assertEqual(projeto.tecnologias.count(), 2)

    def test_projeto_ordering(self):
        projeto_antigo = create_projeto(self.user, titulo='Antigo')
        projeto_novo = create_projeto(self.user, titulo='Novo')
        projetos = list(Projeto.objects.filter(autor=self.user))
        self.assertEqual(projetos[0], projeto_novo)
        self.assertEqual(projetos[1], projeto_antigo)
