from django.shortcuts import render


def calcular_imposto(request):
    return render(request, 'subsTribut/form_calculo.html')
