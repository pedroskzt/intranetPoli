from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission, ContentType
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from intranetPoli.decorators import verificar_permissoes


@login_required
@verificar_permissoes(permissoes_exigidas=['controleAcesso.view_controleacesso'])
def gerenciar_permissoes(request):
    contexto = {'grupos': Group.objects.all()}
    if request.method == 'POST':
        if request.user.has_perm('controleAcesso.change_controleacesso'):
            grupo = get_object_or_404(Group, pk=request.POST['selecionar_grupo'])
            grupo.permissions.set(Permission.objects.filter(pk__in=request.POST.getlist('selecionar_permissoes')))
            contexto['id_grupo'] = grupo.pk
        else:
            messages.error(request, f"Você não possui as permissões necessárias para esta operação. "
                                    f"Caso precise deste acesso, entre em contato com o Departamento de Informática da Matriz.")
    return render(request, 'controleAcesso/permissoes/gerenciar_permissoes.html', context=contexto)


@login_required
@verificar_permissoes(permissoes_exigidas=['controleAcesso.view_controleacesso'])
def ajax_permissoes_grupo(request):
    filtro = False
    if request.method == 'GET':
        grupo = get_object_or_404(Group, pk=request.GET['grupo_id'])
        permissoes_grupo = False
        if grupo:
            permissoes_grupo = [permissao.pk for permissao in grupo.permissions.all()]
        permissoes = []
        for permissao in Permission.objects.all():
            nome = str(permissao).split(' | ')
            permissoes.append({'id': permissao.pk,
                               'nome': f'{nome[1]} | {nome[2]}'})
        filtro = {'permissoes_grupo': permissoes_grupo,
                  'permissoes': sorted(permissoes, key=lambda perm: perm['nome'])}
    return JsonResponse(filtro)


@login_required
@verificar_permissoes(permissoes_exigidas=['controleAcesso.view_controleacesso'])
def ajax_content_type(request):
    filtro = False
    if request.method == 'GET':
        content_types = []
        for content_type in ContentType.objects.all():
            content_types.append({'content_type_id': content_type.pk,
                                  'nome': str(content_type)})
        content_types = sorted(content_types, key=lambda content_type: content_type['nome'])
        filtro = {'content_types': content_types}
    return JsonResponse(filtro)


@login_required
def criar_permissao(request):
    contexto = {'grupos': Group.objects.all()}
    if request.method == 'POST' and request.user.has_perm('controleAcesso.add_controleacesso'):
        contexto['id_grupo'] = int(request.POST['id_grupo'])
        content_type = ContentType.objects.get(pk=request.POST['modelo_selecionado'])
        codinome = request.POST['permissao_nome'].lower().replace(' ', '_')
        if Permission.objects.filter(name=request.POST['permissao_nome']).exists():
            messages.error(request,
                           f'Permissão "{Permission.objects.filter(name=request.POST["permissao_nome"])[0]}" já exise!')
        else:
            try:
                nova_permissao = Permission.objects.create(content_type=content_type,
                                                           name=request.POST['permissao_nome'],
                                                           codename=codinome)
            except Exception as err:
                messages.error(request, f'Erro ao criar permissão: {request.POST["permissao_nome"]}\n{err}')
            else:
                Group.objects.get(pk=request.POST['id_grupo']).permissions.add(nova_permissao)
                nome = str(nova_permissao).split(' | ')
                contexto['permissao'] = {'id': nova_permissao.pk, 'nome': f'{nome[1]} | {nome[2]}'}
    else:
        messages.error(request, f"<p> Você não tem acesso à página ou operação que esta tentando acessar.</p>"
                                f"<p> Caso precise de ter acesso a esta página, contate o Departamento de Informática da Matriz</p>",
                       extra_tags='safe')
    return render(request, 'controleAcesso/permissoes/gerenciar_permissoes.html', context=contexto)


@login_required
def criar_grupo(request):
    contexto = {}
    if request.method == 'POST' and request.user.has_perm('controleAcesso.add_controleacesso'):
        if Group.objects.filter(name=request.POST['grupo_nome']).exists():
            messages.error(request,
                           f'Grupo "{Group.objects.filter(name=request.POST["grupo_nome"])[0]}" já exise!')
        else:
            try:
                novo_grupo = Group.objects.create(name=request.POST['grupo_nome'])
            except Exception as err:
                messages.error(request, f'Erro ao criar grupo: {request.POST["grupo_nome"]}\n{err}')
            else:
                contexto['id_grupo'] = int(novo_grupo.pk)
    else:
        messages.error(request, f"<p> Você não tem acesso à página ou operação que esta tentando acessar.</p>"
                                f"<p> Caso precise de ter acesso a esta página, contate o Departamento de Informática da Matriz</p>",
                       extra_tags='safe')
    contexto['grupos'] = Group.objects.all()
    return render(request, 'controleAcesso/permissoes/gerenciar_permissoes.html', context=contexto)
