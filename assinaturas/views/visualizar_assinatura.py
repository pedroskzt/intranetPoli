from django.shortcuts import render, redirect, get_list_or_404
from assinaturas.forms import AssinaturaForms
from assinaturas.models import Assinatura


def visualizar_assinatura(request):
    if request.method == 'POST':
        form = AssinaturaForms(request.POST)
        if form.is_valid():
            form.save()
            query = Assinatura.objects.filter(nome=form['nome'].value()).get()
            contexto = {'assinatura': query}
            return render(request, 'visualizar_assinatura.html', contexto)
        else:
            contexto = {'form': form}
            return render(request, 'criar_assinatura.html', contexto)
    if request.method == 'GET':
        query = Assinatura.objects.filter(nome=request.GET['buscar'])
        if query.exists():
            contexto = {'assinatura': query.get()}
            return render(request, 'visualizar_assinatura.html', contexto)
        else:
            return render(request, 'index.html')
    return redirect('criar_assinatura')
