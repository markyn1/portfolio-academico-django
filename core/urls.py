from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirecionar_inicio(request):
    return redirect('portfolio:lista_projetos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirecionar_inicio, name='inicio'),
    path('accounts/', include('accounts.urls')),
    path('portfolio/', include('portfolio.urls')),
]