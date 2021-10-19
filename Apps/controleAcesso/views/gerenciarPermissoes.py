from django.contrib.auth.models import Group, Permission
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404


def gerenciar_permissoes(request):
    contexto = {'grupos': Group.objects.all()}
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
            permissoes.append({'grupo_id': permissao.pk,
                               'nome': str(permissao)})

        filtro = {'permissoes_grupo': permissoes_grupo,
                  'permissoes': permissoes}
        print(filtro)
    return JsonResponse(filtro)
