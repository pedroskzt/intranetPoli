from django.shortcuts import render, redirect

from Apps.intranet.forms.form_links import NovoLinkForms
from Apps.intranet.models.links import Links


def painel_intranet(request):
    links = Links.objects.filter(exibir=True)
    return render(request, 'intranet/painel/painel_intranet.html', context={'links': links})


def adicionar_link(request):
    form = None
    if request.method == 'POST':
        form = NovoLinkForms(request.POST, request.FILES)
        print('É POST')
        if request.user.is_authenticated and form.is_valid():
            print("É valido")
            link = form.save(commit=False)
            link.usuario_criacao = request.user
            link.usuario_ultima_alteracao = request.user
            link.save()
            # form.cleaned_data['USUARIO_CRIACAO_ID'] = get_object_or_404(User, pk=request.user.id)
            # form.cleaned_data['USUARIO_ULTIMA_ALTERACAO_ID'] = get_object_or_404(User, pk=request.user.id)

            return redirect('painel_intranet')
        else:
            print('Form Invalido')
    else:
        print('Não É POST')
        form = NovoLinkForms()
    return render(request, 'intranet/painel/adicionar_link.html', context={'forms': form})


def editar_link(request, link_id):
    return redirect('painel_intranet')


def excluir_link(request, link_id):
    return redirect('painel_intranet')
