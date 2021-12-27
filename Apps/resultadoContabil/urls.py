from django.urls import path

from Apps.resultadoContabil.views.resultadoContabil import consulta_cadastro_imposto, cadastro, recalcular

urlpatterns = [
    path('', consulta_cadastro_imposto, name='consulta_cadastro_imposto'),
    path('consultar/', cadastro, name='consultar_cadastro'),
    path('recalcular/', recalcular, name='recalcular_bi'),
]

