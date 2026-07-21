import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProjetoForm
from .models import Projeto, Tecnologia

logger = logging.getLogger('portfolio.security')


@login_required
def lista_projetos_view(request):
    busca = request.GET.get('busca', '')
    projetos = Projeto.objects.all()

    if busca:
        projetos = projetos.filter(titulo__icontains=busca)

    return render(request, 'portfolio/lista_projetos.html', {
        'projetos': projetos,
        'busca': busca
    })


def get_user_projects(user):
    return Projeto.objects.filter(autor=user).order_by('-data_criacao')


@login_required
def detalhe_projeto_view(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    return render(request, 'portfolio/detalhe_projeto.html', {
        'projeto': projeto
    })


@login_required
def criar_projeto_view(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.autor = request.user
            projeto.save()

            lista_tecnologias = form.cleaned_data['tecnologias']
            for nome_tecnologia in lista_tecnologias:
                tecnologia, _ = Tecnologia.objects.get_or_create(nome=nome_tecnologia)
                projeto.tecnologias.add(tecnologia)

            messages.success(request, 'Projeto criado com sucesso.')
            return redirect('portfolio:lista_projetos')
        messages.error(
            request,
            'Não foi possível salvar o projeto. Verifique os campos destacados.'
        )
    else:
        form = ProjetoForm()

    return render(request, 'portfolio/form_projeto.html', {
        'form': form,
        'titulo_pagina': 'Novo Projeto'
    })


@login_required
def editar_projeto_view(request, pk):
    # RS02 — autorização em nível de objeto (IDOR): 404 se não for o autor
    projeto = get_object_or_404(Projeto, pk=pk, autor=request.user)

    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.save()

            projeto.tecnologias.clear()
            lista_tecnologias = form.cleaned_data['tecnologias']

            for nome_tecnologia in lista_tecnologias:
                tecnologia, _ = Tecnologia.objects.get_or_create(nome=nome_tecnologia)
                projeto.tecnologias.add(tecnologia)

            messages.success(request, 'Projeto atualizado com sucesso.')
            return redirect('portfolio:detalhe_projeto', pk=projeto.pk)
        messages.error(
            request,
            'Não foi possível atualizar o projeto. Verifique os campos destacados.'
        )
    else:
        tecnologias_iniciais = ', '.join(
            projeto.tecnologias.values_list('nome', flat=True)
        )

        form = ProjetoForm(instance=projeto, initial={
            'tecnologias': tecnologias_iniciais
        })

    return render(request, 'portfolio/form_projeto.html', {
        'form': form,
        'titulo_pagina': 'Editar Projeto'
    })


@login_required
def excluir_projeto_view(request, pk):
    # RS02 — autorização em nível de objeto (IDOR): 404 se não for o autor
    projeto = get_object_or_404(Projeto, pk=pk, autor=request.user)

    if request.method == 'POST':
        titulo = projeto.titulo
        projeto.delete()
        # RS06 — logging de ação sensível
        logger.info(
            'Usuário %s excluiu o projeto "%s" (pk=%s).',
            request.user.username,
            titulo,
            pk,
        )
        messages.success(request, 'Projeto excluído com sucesso.')
        return redirect('portfolio:lista_projetos')

    return render(request, 'portfolio/confirmar_exclusao.html', {
        'projeto': projeto
    })
