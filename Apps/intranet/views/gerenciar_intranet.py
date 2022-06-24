import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from Apps.intranet.forms.form_links import NovoLinkForms, AtualizaLinkForms
from Apps.intranet.models.links import Links
from intranetPoli.decorators import verificar_permissoes
from intranetPoli.settings import MEDIA_URL


@login_required
@verificar_permissoes(permissoes_exigidas=['intranet.view_links'])
def gerenciar_links(request):
    links = Links.objects.all()
    contexto = {'title': 'Links',
                'links': links}
    return render(request, 'intranet/painel/gerenciar_links.html', context=contexto)


@login_required
@verificar_permissoes(['intranet.add_links'])
def adicionar_link(request):
    contexto = {"title": 'Adicionar Link'}
    if request.method == 'POST':
        form = NovoLinkForms(request.POST, request.FILES)
        if request.user.is_authenticated and form.is_valid():
            link = form.save(commit=False)
            link.usuario_criacao = request.user
            link.usuario_ultima_alteracao = request.user
            link.save()
            form.save_m2m()
            return redirect('gerenciar_links')
    else:
        form = NovoLinkForms()
    contexto['form'] = form
    return render(request, 'intranet/painel/adicionar_link.html', context=contexto)


@login_required
@verificar_permissoes(['intranet.change_links'])
def editar_link(request, link_id):
    contexto = {"title": 'Editar Link',
                'link_id': link_id,
                'media_url': MEDIA_URL,

                }
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
            form.save_m2m()
            return redirect('gerenciar_links')
    contexto['form'] = form

    return render(request, 'intranet/painel/editar_link.html', context=contexto)


@login_required
@verificar_permissoes(['intranet.delete_links'])
def excluir_link(request, link_id):
    link = get_object_or_404(Links, pk=link_id)
    os.remove(link.logo.path)
    link.delete()
    return redirect('gerenciar_links')
