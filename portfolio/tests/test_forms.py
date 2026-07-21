from django.test import TestCase

from portfolio.forms import ProjetoForm
from portfolio.tests.base import projeto_post_data


class ProjetoFormTests(TestCase):
    def test_clean_titulo_valido(self):
        form = ProjetoForm(data=projeto_post_data())
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['titulo'], 'Projeto Django')

    def test_clean_titulo_curto(self):
        form = ProjetoForm(data=projeto_post_data(titulo='abc'))
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)

    def test_clean_integrantes_vazio(self):
        form = ProjetoForm(data=projeto_post_data(integrantes='   ,  '))
        self.assertFalse(form.is_valid())
        self.assertIn('integrantes', form.errors)

    def test_clean_integrantes_valido(self):
        form = ProjetoForm(data=projeto_post_data(integrantes='Ana Silva'))
        self.assertTrue(form.is_valid())

    def test_clean_tecnologias_vazio(self):
        form = ProjetoForm(data=projeto_post_data(tecnologias='  , '))
        self.assertFalse(form.is_valid())
        self.assertIn('tecnologias', form.errors)

    def test_clean_tecnologias_lista(self):
        form = ProjetoForm(data=projeto_post_data(tecnologias='Python, Django'))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['tecnologias'], ['Python', 'Django'])

    def test_clean_tecnologias_com_espacos(self):
        form = ProjetoForm(data=projeto_post_data(tecnologias=' Python ,  Django '))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['tecnologias'], ['Python', 'Django'])

    def test_form_valido_completo(self):
        form = ProjetoForm(data=projeto_post_data())
        self.assertTrue(form.is_valid())
