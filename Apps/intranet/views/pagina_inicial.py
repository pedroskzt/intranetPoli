from django.shortcuts import render
from Apps.intranet.models.links import Links

# Create your blah here.
"""
    Códigos das Paginas:
    0 -> Página inicial;
    1 -> Site Polipeças;
"""


def index(request):
    if request.user.is_authenticated:
        links = Links.objects.filter(exibir=True)
    else:
        links = Links.objects.filter(exibir=True, requer_acesso=False)
    return render(request, 'intranet/index.html', context={'links': links})
