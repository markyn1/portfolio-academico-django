from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.lista_projetos_view, name='lista_projetos'),
    path('novo/', views.criar_projeto_view, name='criar_projeto'),
    path('<int:pk>/', views.detalhe_projeto_view, name='detalhe_projeto'),
    path('<int:pk>/editar/', views.editar_projeto_view, name='editar_projeto'),
    path('<int:pk>/excluir/', views.excluir_projeto_view, name='excluir_projeto'),
]