from django.http import JsonResponse
from Apps.assinaturas.models import Assinatura


def pesquisar_assinatura(request):
    if request.is_ajax():
        term = request.GET.get('term', '')
        query = Assinatura.objects.filter(nome__icontains=term)
        lista_assinaturas = list()
        for assinatura in query:
            lista_assinaturas.append(assinatura.nome)
        return JsonResponse(data=lista_assinaturas, safe=False)
