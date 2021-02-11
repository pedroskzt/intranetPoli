from django.shortcuts import render

from Apps.subsTribut.forms import CalculoForms


def calcular_imposto(request):
    form = CalculoForms()
    contexto = {
        'form': form
    }
    return render(request, 'subsTribut/form_calculo.html', contexto)
