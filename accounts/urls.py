from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
# path(caminho, view, name=nome)
urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
    path('perfil/<str:username>/', views.perfil_publico_view, name='perfil_publico'),
]