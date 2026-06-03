from django.contrib import admin
from .models import Projeto, Tecnologia


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'disciplina', 'status', 'autor', 'data_criacao')
    search_fields = ('titulo', 'disciplina')
    list_filter = ('status', 'data_criacao')
    filter_horizontal = ('tecnologias',)