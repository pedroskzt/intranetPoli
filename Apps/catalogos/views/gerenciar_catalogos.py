import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from Apps.catalogos.forms.form_catalogos import NovoCatalogoForms, AtualizaCatalogoForms
from Apps.catalogos.models.catalogos import Catalogos
from intranetPoli.decorators import verificar_permissoes
from intranetPoli.settings import MEDIA_URL


@login_required
@verificar_permissoes(permissoes_exigidas=['catalogos.view_catalogos'])
def gerenciar_catalogos(request):
    catalogos = Catalogos.objects.all()
    return render(request, 'catalogos/painel/gerenciar_catalogos.html', context={'catalogos': catalogos})


@login_required
@verificar_permissoes(['catalogos.add_catalogos'])
def adicionar_catalogo(request):
    if request.method == 'POST':
        form = NovoCatalogoForms(request.POST, request.FILES)
        if request.user.is_authenticated and form.is_valid():
            catalogo = form.save(commit=False)
            catalogo.usuario_criacao = request.user
            catalogo.usuario_ultima_alteracao = request.user
            catalogo.save()
            return redirect('gerenciar_catalogos')
    else:
        form = NovoCatalogoForms()
    return render(request, 'catalogos/painel/adicionar_catalogo.html', context={'forms': form})


@login_required
@verificar_permissoes(['catalogos.change_catalogos'])
def editar_catalogo(request, catalogo_id):
    if request.method == 'GET':
        catalogo = get_object_or_404(Catalogos, pk=catalogo_id)
        form = AtualizaCatalogoForms(instance=catalogo)
    elif request.method == 'POST':
        catalogo = get_object_or_404(Catalogos, pk=catalogo_id)
        form = AtualizaCatalogoForms(request.POST, request.FILES, instance=catalogo)
        if request.user.is_authenticated and form.is_valid():
            catalogo = form.save(commit=False)
            catalogo.usuario_ultima_alteracao = request.user
            catalogo.save()
            return redirect('gerenciar_catalogos')
    contexto = {
        'forms': form,
        'catalogo_id': catalogo_id,
        'media_url': MEDIA_URL
    }
    return render(request, 'catalogos/painel/editar_catalogo.html', context=contexto)


@login_required
@verificar_permissoes(['catalogos.delete_catalogos'])
def excluir_catalogo(request, catalogo_id):
    catalogo = get_object_or_404(Catalogos, pk=catalogo_id)
    os.remove(catalogo.logo.path)
    catalogo.delete()
    return redirect('gerenciar_catalogos')
