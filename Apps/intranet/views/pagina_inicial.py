from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

from Apps.intranet.models.links import Links


# Create your blah here.


def _query_select_links(pesquisar):
    with connection.cursor() as cursor:
        cursor.execute("ALTER SESSION SET NLS_COMP=LINGUISTIC")
        cursor.execute("ALTER SESSION SET NLS_SORT=BINARY_AI")
        cursor.execute(f"SELECT id "
                       f"FROM intranet_links "
                       f"where titulo like '%{pesquisar}%'")
        retornoBanco = cursor.fetchall()
    return [str(linha[0]) for linha in retornoBanco] if retornoBanco else False


def pagina_inicial(request):
    contexto = {"title": 'Links'}
    if request.user.is_authenticated:
        links = []
        for link in Links.objects.filter(exibir=True):
            if link.permissoes.all():
                permissoes_link = [f"{perm.content_type.app_label}.{perm.codename}" for perm in link.permissoes.all()]
                if request.user.has_perms(permissoes_link):
                    links.append(link)
            else:
                links.append(link)
    else:
        links = Links.objects.filter(exibir=True, requer_acesso=False)
    contexto['links'] = links
    return render(request, 'intranet/pagina_inicial.html', context=contexto)


def ajax_pesquisar_links(request):
    filtro = False
    if request.is_ajax():
        links_id = _query_select_links(request.GET['pesquisar'])
        filtro = {'links_id': links_id if links_id else False}
    return JsonResponse(filtro)
