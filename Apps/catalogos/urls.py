"""subsTribut URL Configuration

"""
from django.urls import path

from Apps.catalogos.views.exibir_catalogos import exibir_catalogos
from Apps.catalogos.views.exibir_catalogos import ajax_pesquisar_catalogos
from Apps.catalogos.views.gerenciar_catalogos import adicionar_catalogo
from Apps.catalogos.views.gerenciar_catalogos import editar_catalogo
from Apps.catalogos.views.gerenciar_catalogos import excluir_catalogo
from Apps.catalogos.views.gerenciar_catalogos import gerenciar_catalogos

urlpatterns = [
    path('', exibir_catalogos, name='exibir_catalogos'),
    path('search/ajax', ajax_pesquisar_catalogos, name='ajax_pesquisar_catalogos'),
    path('painel', gerenciar_catalogos, name='gerenciar_catalogos'),
    path('painel/adicionar', adicionar_catalogo, name='adicionar_catalogo'),
    path('painel/editar/<int:catalogo_id>', editar_catalogo, name='editar_catalogo'),
    path('painel/excluir/<int:catalogo_id>', excluir_catalogo, name='excluir_catalogo'),
]
