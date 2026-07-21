from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import ProfileUpdateForm, RegistroForm, UserUpdateForm
from accounts.models import Profile
from portfolio.tests.base import create_user, registro_post_data


class RegistroFormTests(TestCase):
    def test_registro_valido(self):
        form = RegistroForm(data=registro_post_data())
        self.assertTrue(form.is_valid())

    def test_registro_email_duplicado(self):
        create_user('existente', email='existente@example.com')
        form = RegistroForm(
            data=registro_post_data(
                username='outro',
                email='existente@example.com',
            )
        )
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registro_senhas_diferentes(self):
        data = registro_post_data()
        data['password2'] = 'OutraSenha123!'
        form = RegistroForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class ProfileFormsTests(TestCase):
    def setUp(self):
        self.user = create_user('editor')
        self.profile = Profile.objects.create(
            user=self.user,
            curso='BSI',
            matricula='20240001',
            bio='Bio inicial',
        )

    def test_user_update_valido(self):
        form = UserUpdateForm(
            data={'first_name': 'Nome Atualizado', 'email': 'novo@example.com'},
            instance=self.user,
        )
        self.assertTrue(form.is_valid())

    def test_profile_update_valido(self):
        form = ProfileUpdateForm(
            data={
                'curso': 'Engenharia',
                'matricula': '20249999',
                'bio': 'Nova bio',
            },
            instance=self.profile,
        )
        self.assertTrue(form.is_valid())
