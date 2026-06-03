from django import forms
from .models import Projeto


class ProjetoForm(forms.ModelForm):
    tecnologias = forms.CharField(
        label='Tecnologias',
        help_text='Digite as tecnologias separadas por vírgula. Exemplo: Python, Django, HTML, CSS',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: Python, Django, HTML, CSS'
        })
    )

    class Meta:
        model = Projeto
        fields = [
            'titulo',
            'descricao',
            'disciplina',
            'semestre',
            'status',
            'repositorio',
            'integrantes',
            'tecnologias',
        ]

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        if len(titulo.strip()) < 5:
            raise forms.ValidationError('O título deve ter pelo menos 5 caracteres.')
        return titulo

    def clean_integrantes(self):
        integrantes = self.cleaned_data['integrantes']
        lista = [nome.strip() for nome in integrantes.split(',') if nome.strip()]
        if len(lista) < 1:
            raise forms.ValidationError('Informe pelo menos um integrante.')
        return integrantes

    def clean_tecnologias(self):
        tecnologias = self.cleaned_data['tecnologias']
        lista = [tec.strip() for tec in tecnologias.split(',') if tec.strip()]

        if not lista:
            raise forms.ValidationError('Informe pelo menos uma tecnologia.')

        return lista