from django.shortcuts import render


# Create your views here.
def index(request):
    pagina_selecionada = {"siteAssinatura": {"pagina_guia": 'active'}}
    return render(request, 'assinatura/index.html', pagina_selecionada)
