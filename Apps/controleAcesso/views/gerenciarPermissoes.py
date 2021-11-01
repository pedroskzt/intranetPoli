from django.contrib import messages
from django.contrib.auth.models import Group, Permission, ContentType
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404


def gerenciar_permissoes(request):
    contexto = {'grupos': Group.objects.all()}
    if request.method == 'POST':
        grupo = get_object_or_404(Group, pk=request.POST['selecionar_grupo'])
        grupo.permissions.set(Permission.objects.filter(pk__in=request.POST.getlist('selecionar_permissoes')))
        contexto['id_grupo'] = grupo.pk
    return render(request, 'controleAcesso/permissoes/gerenciar_permissoes.html', context=contexto)


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


def criar_permissao(request):
    contexto = {'grupos': Group.objects.all()}
    if request.method == 'POST':
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

    return render(request, 'controleAcesso/permissoes/gerenciar_permissoes.html', context=contexto)


def criar_grupo(request):
    contexto = {}
    if request.method == 'POST':
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
    contexto['grupos'] = Group.objects.all()
    return render(request, 'controleAcesso/permissoes/gerenciar_permissoes.html', context=contexto)
