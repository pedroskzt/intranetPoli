from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail, BadHeaderError
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Apps.controleAcesso.forms.form_usuario import AtualizaUsuarioForms
from Apps.controleAcesso.forms.form_usuario import NovoUsuarioForms
from intranetPoli.decorators import verificar_permissoes


@login_required
@verificar_permissoes(permissoes_exigidas=['auth.add_user'])
def adicionar_usuario(request):
    """
    View para adição de novos usuários na intranet.
    GET:
        Retorna a página de cadastro de usuário em branco.
    POST:
        Valida os campos preenchidos, testa se a senha e confirmação de senha coincidem, se os campos obrigatorios foram
        preenchidos, cria o cadastro do usuário no banco e retorna para página do painel da intranet.
    :param request:
    :return:
    """
    form = NovoUsuarioForms()
    if request.method == 'POST':
        form = NovoUsuarioForms(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username=form.cleaned_data['usuario'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['senha'],
                                                first_name=form.cleaned_data.get('nome'),
                                                last_name=form.cleaned_data.get('sobrenome'))
            new_user.is_staff = form.cleaned_data['adm_intranet']
            new_user.groups.set(Group.objects.filter(pk__in=form.cleaned_data['groups']))
            new_user.save()
            return redirect('gerenciar_usuarios')

    return render(request, 'controleAcesso/usuarios/adicionar_usuario.html', context={'form': form})


@login_required
def alterar_senha(request):
    """
    View para alterar senha do usuário. Requer estar logado para acessar.
    GET:
        Retorna a página com formulário em branco de alteração de senha.
    POST:
        Verifica se a senha atual está correta, se a nova senha corresponde a confirmação da nova senha, valida se a
        nova senha respeitas os requisitos e retorna para página de login caso esteja tudo certo.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante, finaliza todas as sessões deste usuário.
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('alterar_senha')
        else:
            messages.error(request, 'Favor corrigir os erros destacados.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'controleAcesso/usuarios/alterar_senha.html', {'form': form})


def recuperar_senha(request):
    """
    Recebe os dados de um formulario de recuperação de senha. Verifica se os dados conferem. Caso confira, envia um
    email de recuperação de senha para o email informado.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            usuario = User.objects.filter(email=email)
            if usuario.exists():
                usuario = usuario.get()
                assunto = "Solicitação de recuperação de senha"
                corpo_email = {
                    "email": usuario.email,
                    "domain": "localhost",
                    "site_name": "Intranet Polipeças",
                    "uid": urlsafe_base64_encode(force_bytes(usuario.pk)),
                    "user": usuario,
                    "token": default_token_generator.make_token(usuario),
                    'protocol': 'http',
                }
                email = render_to_string("controleAcesso/usuarios/recuperar_senha.txt", corpo_email)
                try:
                    send_mail(subject=assunto, message=email, from_email='no-reply@polipecas.com.br',
                              recipient_list=[usuario.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            return redirect('recuperar_senha_enviado')
    else:
        form = PasswordResetForm()
    return render(request, 'controleAcesso/usuarios/recuperar_senha.html', {'form': form})


@login_required
@verificar_permissoes(permissoes_exigidas=['auth.view_user'])
def gerenciar_usuarios(request):
    """
    Lista todos os usuários cadastrados na intranet.
    :param request:
    :return:
    """
    usuarios = User.objects.all()
    lista_usuarios = []
    for usuario in usuarios:
        usuario_id = usuario.pk
        nome = usuario.get_full_name()
        nome = usuario.username if nome == '' else nome
        lista_usuarios.append({'id': usuario_id, 'nome': nome})
    contexto = {'lista_usuarios': lista_usuarios}
    return render(request, 'controleAcesso/usuarios/gerenciar_usuarios.html', context=contexto)


@login_required
def editar_usuario(request, usuario_id):
    """
    GET:
    Retorna um formulário com os dados do usúario referente ao usuario_id. Permite que os campos sejam editados.

    POST:
    Verifica se os campos obrigatórios foram preenchidos e alva as alterações no banco.
    :param request:
    :param usuario_id: ID do usuário para edição
    :return:
    """
    if request.user.has_perm('auth.change_user') or request.user.id == usuario_id:
        usuario = get_object_or_404(User, pk=usuario_id)
        contexto = {'usuario_id': usuario_id,
                    'form': AtualizaUsuarioForms(request.user, instance=usuario)}
        if request.method == 'POST':
            form = AtualizaUsuarioForms(request.user, request.POST, instance=usuario)
            if request.user.is_authenticated and form.is_valid():
                form.save()
                messages.success(request, f'Usuário {usuario.get_full_name()} editado com sucesso!')
                contexto['form'] = AtualizaUsuarioForms(request.user, instance=usuario)
            else:
                contexto['form'] = form

        return render(request, 'controleAcesso/usuarios/editar_usuario.html', context=contexto)
    else:
        raise PermissionDenied(f'Permissões exigidas: [\'auth.change_user\']')


@login_required
@verificar_permissoes(permissoes_exigidas=['auth.view_user'])
def ajax_pesquisar_usuarios(request):
    filtro = False
    if request.is_ajax():
        usuarios_id = _query_select_usuarios(request.GET['pesquisar'])
        filtro = {'usuarios_id': usuarios_id if usuarios_id else False}
    return JsonResponse(filtro)


@login_required
@verificar_permissoes(permissoes_exigidas=['auth.view_user'])
def _query_select_usuarios(pesquisar):
    with connection.cursor() as cursor:
        cursor.execute("ALTER SESSION SET NLS_COMP=LINGUISTIC")
        cursor.execute("ALTER SESSION SET NLS_SORT=BINARY_AI")
        cursor.execute(f"SELECT id "
                       f"FROM auth_user "
                       f"where username like '%{pesquisar}%'")
        retornoBanco = cursor.fetchall()
    return [str(linha[0]) for linha in retornoBanco] if retornoBanco else False
