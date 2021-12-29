"""subsTribut URL Configuration

"""
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import path

from Apps.controleAcesso.views.gerenciarPermissoes import ajax_content_type
from Apps.controleAcesso.views.gerenciarPermissoes import ajax_permissoes_grupo
from Apps.controleAcesso.views.gerenciarPermissoes import criar_grupo
from Apps.controleAcesso.views.gerenciarPermissoes import criar_permissao
from Apps.controleAcesso.views.gerenciarPermissoes import gerenciar_permissoes
from Apps.controleAcesso.views.usuario import adicionar_usuario
from Apps.controleAcesso.views.usuario import ajax_pesquisar_usuarios
from Apps.controleAcesso.views.usuario import alterar_senha
from Apps.controleAcesso.views.usuario import editar_usuario
from Apps.controleAcesso.views.usuario import gerenciar_usuarios
from Apps.controleAcesso.views.usuario import recuperar_senha

urlpatterns = [
    path('intranet/usuarios/adicionar', adicionar_usuario, name='adicionar_usuario'),
    path('intranet/usuarios', gerenciar_usuarios, name='gerenciar_usuarios'),
    path('intranet/usuarios/editar/<int:usuario_id>', editar_usuario, name='editar_usuario'),
    path('intranet/usuarios/search/ajax', ajax_pesquisar_usuarios, name='ajax_pesquisar_usuarios'),
    path('intranet/gerenciar/permissoes', gerenciar_permissoes, name='gerenciar_permissoes'),
    path('intranet/gerenciar/permissoes/search/ajax/permissoes', ajax_permissoes_grupo, name='ajax_permissoes_grupo'),
    path('intranet/gerenciar/permissoes/search/ajax/content_type', ajax_content_type, name='ajax_content_type'),
    path('intranet/gerenciar/permissoes/criar/permissao', criar_permissao, name='criar_permissao'),
    path('intranet/gerenciar/permissoes/criar/grupo', criar_grupo, name='criar_grupo'),
    path('intranet/usuarios/alterar/senha', alterar_senha, name='alterar_senha'),
    path('intranet/usuarios/recuperar/senha', recuperar_senha, name='recuperar_senha'),
    path('intranet/usuarios/recuperar/senha/enviado',
         PasswordResetDoneView.as_view(template_name='controleAcesso/usuarios/recuperar_senha_enviado.html'),
         name='recuperar_senha_enviado'),
    path('intranet/usuarios/recuperar/senha/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(template_name='controleAcesso/usuarios/recuperar_senha_confirmacao.html'),
         name='recuperar_senha_confirmacao'),
    path('intranet/usuarios/recuperar/senha/concluido',
         PasswordResetCompleteView.as_view(template_name='controleAcesso/usuarios/recuperar_senha_concluido.html'),
         name='password_reset_complete'),
]
