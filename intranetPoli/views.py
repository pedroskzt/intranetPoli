from django.contrib import messages
from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, 'intranet/errors/404.html', status=404)


def page_access_denied(request, exception):
    messages.error(request, f"<p> Você não tem acesso à página ou operação que esta tentando acessar.</p>"
                            f"<p> Caso precise de ter acesso a esta página, contate o Departamento de Informática da Matriz</p>"
                            f"<p> {exception}",
                   extra_tags='safe')
    return render(request, 'intranet/errors/acesso_negado.html', status=403)
