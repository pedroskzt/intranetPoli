from django.shortcuts import render


def liberar_desconto(request):
    return render(request, 'liberarDesconto/liberar_desconto.html')