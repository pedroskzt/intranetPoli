from django.urls import path

from Apps.intranet.views.gerenciar_intranet import painel_intranet, adicionar_link, editar_link, excluir_link
from Apps.intranet.views.login import login, logout
from Apps.resultadoContabil.views.index import index
from Apps.intranet.views.usuario import adicionar_usuario

urlpatterns = [
    path('', index, name='index-contabil'),
]
