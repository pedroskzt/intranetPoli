"""subsTribut URL Configuration

"""
from django.urls import path

from Apps.catalogos.views import index

urlpatterns = [
    path('', index, name='index_catalogo'),
]
