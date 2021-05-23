from django.shortcuts import render


# Create your views here.
def index(request):
    pagina_selecionada = {"pagina_guia": 'active'}
    return render(request, 'index.html', pagina_selecionada)
