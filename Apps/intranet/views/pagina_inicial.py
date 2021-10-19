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


def index(request):
    if request.user.is_authenticated:
        links = Links.objects.filter(exibir=True)
    else:
        links = Links.objects.filter(exibir=True, requer_acesso=False)
    return render(request, 'intranet/index.html', context={'links': links})


def ajax_pesquisar_links(request):
    filtro = False
    if request.method == 'GET':
        links_id = _query_select_links(request.GET['pesquisar'])
        filtro = {'links_id': links_id if links_id else False}
    return JsonResponse(filtro)
