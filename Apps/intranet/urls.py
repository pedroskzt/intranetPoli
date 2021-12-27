"""subsTribut URL Configuration

"""
from django.urls import path

from Apps.intranet.views.gerenciar_intranet import gerenciar_links, adicionar_link, editar_link, excluir_link
from Apps.intranet.views.log_models import log_models, ajax_log
from Apps.intranet.views.login import login, logout
from Apps.intranet.views.pagina_inicial import pagina_inicial, ajax_pesquisar_links

urlpatterns = [
    path('', pagina_inicial, name='pagina_inicial'),
    path('intranet/painel/search/ajax', ajax_pesquisar_links, name='ajax_pesquisar_links'),
    path('intranet/usuario/login/next', login, name='login'),
    path('intranet/usuario/logout', logout, name='logout'),
    path('intranet/painel', gerenciar_links, name='gerenciar_links'),
    path('intranet/painel/adicionar/link', adicionar_link, name='adicionar_link'),
    path('intranet/painel/editar/<int:link_id>', editar_link, name='editar_link'),
    path('intranet/painel/excluir/<int:link_id>', excluir_link, name='excluir_link'),
    path('cpd/painel/log/<str:model>/<str:tabela>/<str:changelist>', log_models, name='log_models'),
    path('cpd/painel/log/ajax', ajax_log, name='ajax_log'),

]
