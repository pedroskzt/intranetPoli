from django.contrib import messages
from django.db import connections
from django.db.utils import DatabaseError
from django.shortcuts import render, redirect

from Apps.resultadoContabil.forms.form_cadastro import FormConsultaCadastro


def index(request):
    return render(request, 'resultadoContabil/index.html')