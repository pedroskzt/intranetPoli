from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

from Apps.catalogos.models.catalogos import Catalogos

# Create your blah here.


def _query_select_catalogos(pesquisar):
    with connection.cursor() as cursor:
        cursor.execute("ALTER SESSION SET NLS_COMP=LINGUISTIC")
        cursor.execute("ALTER SESSION SET NLS_SORT=BINARY_AI")
        cursor.execute(f"SELECT id "
                       f"FROM catalogos_catalogos "
                       f"where titulo like '%{pesquisar}%'")
        retornoBanco = cursor.fetchall()
    return [str(linha[0]) for linha in retornoBanco] if retornoBanco else False


def exibir_catalogos(request):
    contexto = {"title": 'Catálogos'}
    catalogos = Catalogos.objects.filter(exibir=True)
    contexto['catalogos'] = catalogos
    return render(request, 'catalogos/catalogos.html', context=catalogos)


def ajax_pesquisar_catalogos(request):
    filtro = False
    if request.is_ajax():
        catalogo_id = _query_select_catalogos(request.GET['pesquisar'])
        filtro = {'catalogo_id': catalogo_id if catalogo_id else False}
    return JsonResponse(filtro)
