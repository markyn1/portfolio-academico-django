from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile
from portfolio.tests.base import create_projeto, create_user, registro_post_data


class AccountsViewsTests(TestCase):
    def setUp(self):
        self.user = create_user('marcos', email='marcos@example.com')
        self.profile = Profile.objects.create(
            user=self.user,
            curso='BSI',
            matricula='20240001',
            bio='Bio teste',
        )

    def test_registro_get_anonimo(self):
        response = self.client.get(reverse('accounts:registro'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cadastro')

    def test_registro_post_valido(self):
        response = self.client.post(
            reverse('accounts:registro'),
            registro_post_data(username='novo', email='novo@example.com'),
        )
        self.assertRedirects(response, reverse('portfolio:lista_projetos'))
        self.assertTrue(User.objects.filter(username='novo').exists())
        self.assertTrue(Profile.objects.filter(user__username='novo').exists())

    def test_registro_post_invalido(self):
        response = self.client.post(
            reverse('accounts:registro'),
            registro_post_data(username='marcos', email='marcos@example.com'),
        )
        self.assertEqual(response.status_code, 200)
        messages = [message.message for message in get_messages(response.wsgi_request)]
        self.assertTrue(
            any('Não foi possível concluir o cadastro' in message for message in messages)
        )

    def test_registro_redirect_se_logado(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:registro'))
        self.assertRedirects(response, reverse('portfolio:lista_projetos'))

    def test_perfil_requer_login(self):
        response = self.client.get(reverse('accounts:perfil'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_perfil_get_com_projetos(self):
        create_projeto(self.user, titulo='Meu Projeto Perfil')
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_meu_perfil'])
        self.assertContains(response, 'Meu Projeto Perfil')

    def test_perfil_publico_outro_usuario(self):
        outro = create_user('ana', email='ana@example.com')
        create_projeto(outro, titulo='Projeto da Ana')
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('accounts:perfil_publico', args=['ana'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_meu_perfil'])
        self.assertContains(response, 'Projeto da Ana')

    def test_perfil_publico_proprio_redirect(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('accounts:perfil_publico', args=['marcos'])
        )
        self.assertRedirects(response, reverse('accounts:perfil'))

    def test_perfil_publico_404(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('accounts:perfil_publico', args=['inexistente'])
        )
        self.assertEqual(response.status_code, 404)

    def test_editar_perfil_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:editar_perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_form', response.context)
        self.assertIn('profile_form', response.context)

    def test_editar_perfil_post_valido(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('accounts:editar_perfil'),
            {
                'first_name': 'Marcos Atualizado',
                'email': 'atualizado@example.com',
                'curso': 'Sistemas',
                'matricula': '20249999',
                'bio': 'Bio atualizada',
            },
        )
        self.assertRedirects(response, reverse('accounts:perfil'))
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Marcos Atualizado')
        self.assertEqual(self.profile.curso, 'Sistemas')

    def test_editar_perfil_post_invalido(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('accounts:editar_perfil'),
            {
                'first_name': 'Marcos',
                'email': 'email-invalido',
                'curso': 'Sistemas',
                'matricula': '20249999',
                'bio': 'Bio',
            },
        )
        self.assertEqual(response.status_code, 200)
        messages = [message.message for message in get_messages(response.wsgi_request)]
        self.assertTrue(
            any('Não foi possível salvar o perfil' in message for message in messages)
        )

    def test_login_post_valido(self):
        response = self.client.post(
            reverse('accounts:login'),
            {'username': 'marcos', 'password': 'senha12345'},
        )
        self.assertRedirects(response, reverse('portfolio:lista_projetos'))

    def test_login_post_invalido(self):
        response = self.client.post(
            reverse('accounts:login'),
            {'username': 'marcos', 'password': 'senha_errada'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'corretos')

    def test_logout_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('accounts:login'))
