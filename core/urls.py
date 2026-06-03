from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirecionar_inicio(request):
    if request.user.is_authenticated:
        return redirect('portfolio:lista_projetos')
    return redirect('accounts:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirecionar_inicio, name='inicio'),
    path('accounts/', include('accounts.urls')),
    path('portfolio/', include('portfolio.urls')),
]