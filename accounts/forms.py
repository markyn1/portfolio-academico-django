from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegistroForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'As senhas informadas não coincidem.',
    }

    first_name = forms.CharField(
        label='Nome',
        max_length=150
    )
    username = forms.CharField(
        label='Nome de usuário',
        max_length=150,
        help_text='Obrigatório. Até 150 caracteres. Letras, números e os símbolos @/./+/-/_ .'
    )
    email = forms.EmailField(
        label='E-mail',
        required=True
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput,
        help_text=(
            '<ul>'
            '<li>Sua senha não pode ser muito parecida com suas informações pessoais.</li>'
            '<li>Sua senha deve conter pelo menos 8 caracteres.</li>'
            '<li>Sua senha não pode ser uma senha muito comum.</li>'
            '<li>Sua senha não pode ser totalmente numérica.</li>'
            '</ul>'
        )
    )
    password2 = forms.CharField(
        label='Confirmação de senha',
        widget=forms.PasswordInput,
        help_text='Digite a mesma senha informada acima para confirmação.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com este e-mail.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].error_messages = {
            'required': 'Informe um nome de usuário.',
            'unique': 'Este nome de usuário já está em uso.',
        }

        self.fields['password1'].error_messages = {
            'required': 'Informe uma senha.',
        }

        self.fields['password2'].error_messages = {
            'required': 'Confirme a senha.',
        }

        self.fields['first_name'].error_messages = {
            'required': 'Informe seu nome.',
        }

        self.fields['email'].error_messages = {
            'required': 'Informe um e-mail.',
            'invalid': 'Informe um e-mail válido.',
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = User
        fields = ['first_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    curso = forms.CharField(label='Curso', required=False)
    matricula = forms.CharField(label='Matrícula', required=False)
    bio = forms.CharField(label='Biografia', required=False, widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ['curso', 'matricula', 'bio']