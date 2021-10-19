"""subsTribut URL Configuration

"""
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import path

from Apps.controleAcesso.views.usuario import adicionar_usuario
from Apps.controleAcesso.views.usuario import alterar_senha
from Apps.controleAcesso.views.usuario import editar_usuario
from Apps.controleAcesso.views.usuario import listar_usuarios
from Apps.controleAcesso.views.usuario import recuperar_senha
from Apps.controleAcesso.views.usuario import ajax_pesquisar_usuarios
from Apps.controleAcesso.views.gerenciarPermissoes import ajax_permissoes_grupo
from Apps.controleAcesso.views.gerenciarPermissoes import gerenciar_permissoes

urlpatterns = [
    path('intranet/usuario/adicionar', adicionar_usuario, name='adicionar_usuario'),
    path('intranet/usuario/listar', listar_usuarios, name='listar_usuarios'),
    path('intranet/usuario/editar/<int:usuario_id>', editar_usuario, name='editar_usuario'),
    path('intranet/usuario/search/ajax', ajax_pesquisar_usuarios, name='ajax_pesquisar_usuarios'),
    path('intranet/gerenciar/permissoes', gerenciar_permissoes, name='gerenciar_permissoes'),
    path('intranet/gerenciar/permissoes/search/ajax', ajax_permissoes_grupo, name='ajax_permissoes_grupo'),
    path('intranet/usuario/alterar/senha', alterar_senha, name='alterar_senha'),
    path('intranet/usuario/recuperar/senha', recuperar_senha, name='recuperar_senha'),
    path('intranet/usuario/recuperar/senha/enviado',
         PasswordResetDoneView.as_view(template_name='controleAcesso/usuarios/recuperar_senha_enviado.html'),
         name='recuperar_senha_enviado'),
    path('intranet/usuario/recuperar/senha/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(template_name='controleAcesso/usuarios/recuperar_senha_confirmacao.html'),
         name='recuperar_senha_confirmacao'),
    path('intranet/usuario/recuperar/senha/concluido',
         PasswordResetCompleteView.as_view(template_name='controleAcesso/usuarios/recuperar_senha_concluido.html'),
         name='password_reset_complete'),
]

