from django.shortcuts import render

from Apps.assinaturas.forms import AssinaturaForms


def criar_assinatura(request):
    form = AssinaturaForms()
    contexto = {"siteAssinatura": {"pagina_criar": 'active',
                                   'form': form}}
    return render(request, "assinatura/criar_assinatura.html", contexto)
