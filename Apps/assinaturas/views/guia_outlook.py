from django.shortcuts import render


def guia_outlook(request):
    pagina_selecionada = {"siteAssinatura": {"pagina_guias": 'active',
                                             "guia_outlook": 'active'}}
    return render(request, 'assinatura/guias/guia_outlook.html', pagina_selecionada)
