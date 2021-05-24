from django.shortcuts import render


def guia_outlook(request):
    pagina_selecionada = {
        "pagina_guias": 'active',
        "guia_outlook": 'active'
    }
    return render(request, 'guias/guia_outlook.html', pagina_selecionada)

