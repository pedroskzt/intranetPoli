import os

from django.shortcuts import render, redirect, get_object_or_404

from Apps.intranet.forms.form_links import NovoLinkForms, AtualizaLinkForms
from Apps.intranet.models.links import Links
from intranetPoli.settings import MEDIA_URL


def painel_intranet(request):
    links = Links.objects.all()
    return render(request, 'intranet/painel/painel_intranet.html', context={'links': links})


def adicionar_link(request):
    if request.method == 'POST':
        form = NovoLinkForms(request.POST, request.FILES)
        if request.user.is_authenticated and form.is_valid():
            link = form.save(commit=False)
            link.usuario_criacao = request.user
            link.usuario_ultima_alteracao = request.user
            link.save()
            return redirect('painel_intranet')
    else:
        form = NovoLinkForms()
    return render(request, 'intranet/painel/adicionar_link.html', context={'forms': form})


def editar_link(request, link_id):
    if request.method == 'GET':
        link = get_object_or_404(Links, pk=link_id)
        form = AtualizaLinkForms(instance=link)

    elif request.method == 'POST':
        link = get_object_or_404(Links, pk=link_id)
        form = AtualizaLinkForms(request.POST, request.FILES, instance=link)
        if request.user.is_authenticated and form.is_valid():
            link = form.save(commit=False)
            link.usuario_ultima_alteracao = request.user
            link.save()
            return redirect('painel_intranet')
    contexto = {
        'forms': form,
        'link_id': link_id,
        'media_url': MEDIA_URL
    }
    return render(request, 'intranet/painel/editar_link.html', context=contexto)


def excluir_link(request, link_id):
    # TODO: Adicionar modal de confirmação de exclusão
    link = get_object_or_404(Links, pk=link_id)
    os.remove(link.logo.path)
    link.delete()
    return redirect('painel_intranet')
