"""subsTribut URL Configuration

"""
from django.contrib import admin
from django.urls import path
from Apps.liberarDesconto.views import liberar_desconto

urlpatterns = [
    path('', liberar_desconto, name='liberar_desconto'),
]
