from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from portfolio.views import get_user_projects

from .forms import RegistroForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('portfolio:lista_projetos')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.save()

            Profile.objects.create(user=user)

            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso.')
            return redirect('portfolio:lista_projetos')
        messages.error(
            request,
            'Não foi possível concluir o cadastro. Verifique os campos destacados.'
        )
    else:
        form = RegistroForm()

    return render(request, 'accounts/registro.html', {'form': form})


@login_required
def perfil_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    return render(request, 'accounts/perfil.html', {
        'perfil_usuario': request.user,
        'profile': profile,
        'projetos': get_user_projects(request.user),
        'is_meu_perfil': True,
    })


@login_required
def perfil_publico_view(request, username):
    perfil_usuario = get_object_or_404(User, username=username)

    if perfil_usuario == request.user:
        return redirect('accounts:perfil')

    profile, _ = Profile.objects.get_or_create(user=perfil_usuario)

    return render(request, 'accounts/perfil.html', {
        'perfil_usuario': perfil_usuario,
        'profile': profile,
        'projetos': get_user_projects(perfil_usuario),
        'is_meu_perfil': False,
    })


@login_required
def editar_perfil_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil atualizado com sucesso.')
            return redirect('accounts:perfil')
        messages.error(
            request,
            'Não foi possível salvar o perfil. Verifique os campos destacados.'
        )
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/editar_perfil.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })