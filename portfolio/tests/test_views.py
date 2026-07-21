from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from portfolio.models import Projeto, Tecnologia
from portfolio.tests.base import create_projeto, create_user, projeto_post_data
from portfolio.views import get_user_projects


class PortfolioViewsTests(TestCase):
    def setUp(self):
        self.client = self.client
        self.user = create_user('autor')
        self.outro = create_user('outro')
        self.projeto = create_projeto(self.user, titulo='Projeto Alpha')

    def test_lista_requer_login(self):
        response = self.client.get(reverse('portfolio:lista_projetos'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_lista_get_200(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('portfolio:lista_projetos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projeto Alpha')

    def test_lista_busca_por_titulo(self):
        create_projeto(self.user, titulo='Outro Titulo')
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('portfolio:lista_projetos'),
            {'busca': 'Alpha'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projeto Alpha')
        self.assertNotContains(response, 'Outro Titulo')

    def test_lista_busca_sem_resultado(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('portfolio:lista_projetos'),
            {'busca': 'inexistente'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhum projeto encontrado')

    def test_detalhe_200(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('portfolio:detalhe_projeto', args=[self.projeto.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projeto Alpha')

    def test_detalhe_404(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('portfolio:detalhe_projeto', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_criar_get_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('portfolio:criar_projeto'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Novo Projeto')

    def test_criar_post_valido(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('portfolio:criar_projeto'),
            projeto_post_data(titulo='Novo Projeto Criado'),
        )
        self.assertRedirects(response, reverse('portfolio:lista_projetos'))
        projeto = Projeto.objects.get(titulo='Novo Projeto Criado')
        self.assertEqual(projeto.autor, self.user)
        self.assertEqual(projeto.tecnologias.count(), 2)
        self.assertTrue(Tecnologia.objects.filter(nome='Python').exists())

    def test_criar_post_invalido(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('portfolio:criar_projeto'),
            projeto_post_data(titulo='abc'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Não foi possível salvar o projeto',
        )

    def test_editar_get_autor(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('portfolio:editar_projeto', args=[self.projeto.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editar Projeto')
        self.assertContains(response, 'Python')

    def test_editar_post_autor(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('portfolio:editar_projeto', args=[self.projeto.pk]),
            projeto_post_data(
                titulo='Projeto Atualizado',
                tecnologias='Django, HTML',
            ),
        )
        self.assertRedirects(
            response,
            reverse('portfolio:detalhe_projeto', args=[self.projeto.pk]),
        )
        self.projeto.refresh_from_db()
        self.assertEqual(self.projeto.titulo, 'Projeto Atualizado')
        self.assertEqual(
            set(self.projeto.tecnologias.values_list('nome', flat=True)),
            {'Django', 'HTML'},
        )

    def test_editar_post_invalido(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('portfolio:editar_projeto', args=[self.projeto.pk]),
            projeto_post_data(titulo='abc'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Não foi possível atualizar o projeto',
        )

    def test_editar_negado_outro_usuario(self):
        self.client.force_login(self.outro)
        response = self.client.get(
            reverse('portfolio:editar_projeto', args=[self.projeto.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_excluir_get_confirmacao(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('portfolio:excluir_projeto', args=[self.projeto.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projeto Alpha')

    def test_excluir_post_autor(self):
        self.client.force_login(self.user)
        projeto_pk = self.projeto.pk
        response = self.client.post(
            reverse('portfolio:excluir_projeto', args=[projeto_pk])
        )
        self.assertRedirects(response, reverse('portfolio:lista_projetos'))
        self.assertFalse(Projeto.objects.filter(pk=projeto_pk).exists())

    def test_excluir_negado_outro_usuario(self):
        self.client.force_login(self.outro)
        response = self.client.post(
            reverse('portfolio:excluir_projeto', args=[self.projeto.pk])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Projeto.objects.filter(pk=self.projeto.pk).exists())

    def test_get_user_projects(self):
        create_projeto(self.user, titulo='Segundo Projeto')
        create_projeto(self.outro, titulo='Projeto Outro')
        projetos = list(get_user_projects(self.user))
        self.assertEqual(len(projetos), 2)
        self.assertTrue(all(projeto.autor == self.user for projeto in projetos))
