"""subsTribut URL Configuration

"""
from django.contrib import admin
from django.urls import path
from Apps.subsTribut.views.calcular_imposto import calcular_imposto

urlpatterns = [
    path('', calcular_imposto, name='calcular_imposto')
]
