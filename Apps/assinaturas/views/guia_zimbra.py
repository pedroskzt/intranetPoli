from django.shortcuts import render


def guia_zimbra(request):
    pagina_selecionada = {"siteAssinatura": {"pagina_guias": 'active',
                                             "guia_zimbra": 'active'}}
    return render(request, "assinatura/guias/guia_zimbra.html", pagina_selecionada)
