from django.shortcuts import render
from django.http import JsonResponse

from assinaturas.models import Assinatura


def pesquisar_assinatura(request):
    if request.is_ajax():
        term = request.GET.get('term', '')
        query = Assinatura.objects.filter(nome__icontains=term)
        lista_assinaturas = list()
        for assinatura in query:
            lista_assinaturas.append(assinatura.nome)
        return JsonResponse(data=lista_assinaturas, safe=False)

    # if request.method == 'GET':
    #     print(request.GET.get('term'))
    #     query = Assinatura.objects.filter(nome__icontains=request.GET.get('term'))
    #     print(query)
    #     lista_assinaturas = list()
    #     for assinatura in query:
    #         lista_assinaturas.append(assinatura.nome)
    #     # pagina_selecionada = {"pagina_pesquisar": 'active'}
    #     # return render(request, 'pesquisar_assinatura.html', pagina_selecionada)
    #     return JsonResponse(data=lista_assinaturas, safe=False)




