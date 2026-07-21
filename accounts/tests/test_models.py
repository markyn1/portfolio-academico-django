from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Profile


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='maria',
            password='senha12345',
            email='maria@example.com',
        )

    def test_profile_str(self):
        profile = Profile.objects.create(user=self.user, curso='BSI')
        self.assertEqual(str(profile), 'Perfil de maria')

    def test_profile_campos_opcionais(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.curso, '')
        self.assertEqual(profile.matricula, '')
        self.assertEqual(profile.bio, '')
