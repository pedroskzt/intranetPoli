from django.shortcuts import render, redirect, get_list_or_404
from Apps.assinaturas.forms import AssinaturaForms
from Apps.assinaturas.models import Assinatura


def visualizar_assinatura(request):
    if request.method == 'POST':
        form = AssinaturaForms(request.POST)
        if form.is_valid():
            form.save()
            query = Assinatura.objects.filter(nome=form['nome'].value()).get()
            contexto = {"siteAssinatura": {'assinatura': query}}
            return render(request, 'assinatura/visualizar_assinatura.html', contexto)
        else:
            contexto = {"siteAssinatura": {'form': form}}
            return render(request, 'assinatura/criar_assinatura.html', contexto)
    if request.method == 'GET':
        print(request.GET['buscar'])
        query = Assinatura.objects.filter(nome=request.GET['buscar'])
        if query.exists():
            contexto = {"siteAssinatura": {'assinatura': query.get()}}
            return render(request, 'assinatura/visualizar_assinatura.html', contexto)
        else:
            return redirect('index_assinatura')
    return redirect('criar_assinatura')
