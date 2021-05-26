from django.shortcuts import render


# Create your views here.
def guia_thunderbird(request):
    pagina_selecionada = {"siteAssinatura": {"pagina_guias": 'active',
                                             "guia_thunderbird": 'active'}}
    return render(request, 'assinatura/guias/guia_thunderbird.html', pagina_selecionada)
