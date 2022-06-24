from django.shortcuts import render, redirect

from Apps.assinaturas.forms.cadastrar_assinatura import AssinaturaForms
from Apps.assinaturas.models.assinaturas_email import Assinatura


def assinaturas_email(request):
    assinaturas = [{"id": assinatura.id, "nome": assinatura.nome} for assinatura in Assinatura.objects.all()]
    contexto = {"title": 'Assinaturas'}

    return render(request, 'assinatura/assinaturas_email.html', context=contexto)


def criar_assinatura(request):
    form = AssinaturaForms()
    assinaturas = [{"id": assinatura.id, "nome": assinatura.nome} for assinatura in Assinatura.objects.all()]
    contexto = {"title": 'Assinaturas',
                "siteAssinatura": {"pagina_criar": 'active'},
                "form": form}

    if request.method == 'POST':
        form = AssinaturaForms(request.POST)
        if form.is_valid():
            form.save()
            query = Assinatura.objects.filter(nome=form.cleaned_data['nome']).get()
            contexto['assinatura'] = query
            contexto['siteAssinatura'] = ''
            return render(request, 'assinatura/visualizar_assinatura.html', contexto)
        contexto['form'] = form
    return render(request, "assinatura/criar_assinatura.html", contexto)


def visualizar_assinatura(request):
    assinaturas = [{"id": assinatura.id, "nome": assinatura.nome} for assinatura in Assinatura.objects.all()]
    query = Assinatura.objects.filter(pk=request.GET['buscar'])
    if query.exists():
        contexto = {"title": 'Assinaturas',
                    'assinatura': query.get()}
        return render(request, 'assinatura/visualizar_assinatura.html', contexto)
    else:
        return redirect('assinaturas_email')


def tutoriais(request, programa_email):
    assinaturas = [{"id": assinatura.id, "nome": assinatura.nome} for assinatura in Assinatura.objects.all()]
    contexto = {"title": 'Assinaturas',
                "pagina_tutoriais": 'active',
                "programa_email": programa_email}
    return render(request, f"assinatura/guias/{programa_email}.html", context=contexto)
