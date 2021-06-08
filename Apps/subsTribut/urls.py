"""subsTribut URL Configuration

"""
from django.contrib import admin
from django.urls import path
from Apps.subsTribut.views.calcular_imposto import CalcularView

urlpatterns = [
    path('', CalcularView.as_view(), name='index_st'),
    path('', CalcularView.as_view(), name='calcular_imposto_individual'),
    path('numr_negociacao', CalcularView.as_view(), name='calcular_neg_vw'),
]
