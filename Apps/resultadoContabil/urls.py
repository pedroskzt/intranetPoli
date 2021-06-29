from django.urls import path

from Apps.resultadoContabil.views.index import index, cadastro, recalcular

urlpatterns = [
    path('', index, name='index_contabil'),
    path('consultar/', cadastro, name='consultar_cadastro'),
    path('recalcular/', recalcular, name='recalcular_bi'),
]

