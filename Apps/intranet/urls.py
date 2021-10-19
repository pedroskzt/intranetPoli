"""subsTribut URL Configuration

"""
from django.urls import path

from Apps.intranet.views.gerenciar_intranet import painel_intranet, adicionar_link, editar_link, excluir_link
from Apps.intranet.views.log_models import log_models, ajax_log
from Apps.intranet.views.login import login, logout
from Apps.intranet.views.pagina_inicial import index, ajax_pesquisar_links

urlpatterns = [
    path('', index, name='pagina_inicial'),
    path('intranet/usuario/login/next', login, name='login'),
    path('intranet/usuario/logout', logout, name='logout'),
    path('painel/intranet', painel_intranet, name='painel_intranet'),
    path('painel/intranet/adicionar/link', adicionar_link, name='adicionar_link'),
    path('painel/intranet/editar/<int:link_id>', editar_link, name='editar_link'),
    path('painel/intranet/excluir/<int:link_id>', excluir_link, name='excluir_link'),
    path('painel/cpd/log/<str:model>/<str:tabela>/<str:changelist>', log_models, name='log_models'),
    path('painel/cpd/log/ajax', ajax_log, name='ajax_log'),
    path('home/search/ajax', ajax_pesquisar_links, name='ajax_pesquisar_links'),
]

