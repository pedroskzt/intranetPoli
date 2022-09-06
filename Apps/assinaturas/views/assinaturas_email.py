from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Apps.assinaturas.forms.form_assinaturas import CriaAssinaturaForms, EditarAssinaturaForms
from Apps.assinaturas.models.assinaturas_email import Assinatura
from intranetPoli.decorators import verificar_permissoes


def assinaturas_email(request):
    assinaturas = [{"id": assinatura.id, "nome": assinatura.nome} for assinatura in Assinatura.objects.all()]
    contexto = {"title": 'Assinaturas',
                "assinaturas": assinaturas}

    return render(request, 'assinatura/assinaturas_email.html', context=contexto)


def criar_assinatura(request):
    form = CriaAssinaturaForms()
    assinaturas = [{"id": assinatura.id, "nome": assinatura.nome} for assinatura in Assinatura.objects.all()]
    contexto = {"title": 'Assinaturas',
                "siteAssinatura": {"pagina_criar": 'active'},
                "form": form,
                "assinaturas": assinaturas}

    if request.method == 'POST':
        form = CriaAssinaturaForms(request.POST)
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
                    'assinatura': query.get(),
                    "assinaturas": assinaturas}
        return render(request, 'assinatura/visualizar_assinatura.html', contexto)
    else:
        return redirect('assinaturas_email')


@login_required
@verificar_permissoes(['assinaturas.change_assinatura'])
def editar_assinatura(request, assinatura_id):
    assinaturas = [{"id": assinatura.id, "nome": assinatura.nome} for assinatura in Assinatura.objects.all()]
    contexto = {"title": 'Editar Assinaturas',
                "assinatura_id": assinatura_id,
                "assinaturas": assinaturas}

    if request.method == 'GET':
        assinatura = get_object_or_404(Assinatura, pk=assinatura_id)
        form = EditarAssinaturaForms(instance=assinatura)

    elif request.method == 'POST':
        assinatura = get_object_or_404(Assinatura, pk=assinatura_id)
        form = EditarAssinaturaForms(request.POST, request.FILES, instance=assinatura)
        if request.user.is_authenticated and form.is_valid():
            form.save()
            messages.success(request, f'Assinatura {assinatura.nome} editada com sucesso!')

    contexto['form'] = form

    return render(request, "assinatura/editar_assinatura.html", contexto)


def tutoriais(request, programa_email):
    assinaturas = [{"id": assinatura.id, "nome": assinatura.nome} for assinatura in Assinatura.objects.all()]
    contexto = {"title": 'Assinaturas',
                "pagina_tutoriais": 'active',
                "programa_email": programa_email,
                "assinaturas": assinaturas}
    return render(request, f"assinatura/guias/{programa_email}.html", context=contexto)
