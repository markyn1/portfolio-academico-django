from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Tecnologia(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Tecnologia'
        verbose_name_plural = 'Tecnologias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    STATUS_CHOICES = [
        ('planejamento', 'Planejamento'),
        ('em_andamento', 'Em andamento'),
        ('concluido', 'Concluído'),
        ('pausado', 'Pausado'),
    ]

    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projetos'
    )
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(validators=[MinLengthValidator(10)])
    disciplina = models.CharField(max_length=100)
    semestre = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    repositorio = models.URLField(blank=True, null=True)
    integrantes = models.TextField(
        help_text='Informe os nomes dos integrantes separados por vírgula.'
    )
    tecnologias = models.ManyToManyField(Tecnologia, related_name='projetos')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo