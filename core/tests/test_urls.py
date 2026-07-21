from django.test import TestCase
from django.urls import reverse

from portfolio.tests.base import create_user


class CoreUrlsTests(TestCase):
    def test_inicio_anonimo_redirect_login(self):
        response = self.client.get(reverse('inicio'))
        self.assertRedirects(response, reverse('accounts:login'))

    def test_inicio_autenticado_redirect_lista(self):
        user = create_user('visitante')
        self.client.force_login(user)
        response = self.client.get(reverse('inicio'))
        self.assertRedirects(response, reverse('portfolio:lista_projetos'))
