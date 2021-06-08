"""subsTribut URL Configuration

"""
from django.urls import path

from Apps.intranet.views.gerenciar_intranet import painel_intranet, adicionar_link, editar_link, excluir_link
from Apps.intranet.views.login import login, logout
from Apps.intranet.views.pagina_inicial import index

urlpatterns = [
    path('', index, name='pagina_inicial'),
    path('login/next', login, name='login'),
    path('logout', logout, name='logout'),
    path('painel/intranet', painel_intranet, name='painel_intranet'),
    path('painel/intranet/adicionar', adicionar_link, name='adicionar_link'),
    path('painel/intranet/editar/<int:link_id>', editar_link, name='editar_link'),
    path('painel/intranet/excluir/<int:link_id>', excluir_link, name='excluir_link'),
]
