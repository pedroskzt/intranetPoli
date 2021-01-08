from django.shortcuts import render


# Create your views here.
def guia_thunderbird(request):
    pagina_selecionada = {
        "pagina_guias": 'active',
        "guia_thunderbird": 'active'
    }
    return render(request, 'guias/guia_thunderbird.html', pagina_selecionada)
