from django.shortcuts import render, redirect
from assinaturas.forms import AssinaturaForms


def visualizar_assinatura(request):
    if request.method == 'POST':
        form = AssinaturaForms(request.POST)
        if form.is_valid():
            form.save()
            contexto = {'form': form}
            return render(request, 'visualizar_assinatura.html', contexto)
        else:
            contexto = {'form': form}
            return render(request, 'criar_assinatura.html', contexto)
    return redirect('criar_assinatura')
