from django.shortcuts import render


def guia_zimbra(request):
    pagina_selecionada = {
        "pagina_guias": 'active',
        "guia_zimbra": 'active'
    }
    return render(request, "guias/guia_zimbra.html", pagina_selecionada)
