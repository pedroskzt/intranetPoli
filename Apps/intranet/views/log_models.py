import json
from datetime import datetime

from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import make_aware

from Apps.subsTribut.models import Tributos
from Apps.subsTribut.templatetags import formatar_porcentagem
from intranetPoli.decorators import verificar_permissoes

MODELOS = {}


@login_required
@verificar_permissoes(permissoes_exigidas=['subsTribut.view_tributos', 'subsTribut.view_historicaltributos'])
def log_models(request, model, tabela, changelist):
    contexto = {}
    if request.method == 'GET':
        contexto['breadcrumb'] = {'modelo': model,
                                  'tabela': tabela,
                                  'changelist': changelist}
        if model not in MODELOS:
            contexto['page_404'] = True
    return render(request, 'intranet/painel/log_models.html', context=contexto)


@login_required
@verificar_permissoes(permissoes_exigidas=['subsTribut.view_tributos', 'subsTribut.view_historicaltributos'])
def ajax_log(request):
    log = {}
    if request.method == 'GET':
        log = MODELOS[request.GET['modelo']](request)
    return JsonResponse(log)


def _subs_tribut(request):
    log = {}
    data_inicial = make_aware(datetime.strptime(request.GET['data_inicial'], '%Y-%m-%d'))
    data_final = make_aware(datetime.strptime(f"{request.GET['data_final']} 23:59:59", '%Y-%m-%d %H:%M:%S'))
    log['data_inicial'] = data_inicial.date()
    log['data_final'] = data_final.date()
    log_list = []
    for tributos, log_entry in zip(
            Tributos.history.filter(history_date__gt=data_inicial, history_date__lt=data_final),
            LogEntry.objects.filter(action_time__gt=data_inicial, action_time__lt=data_final)):
        alterados = {}
        if tributos.history_type == '~' or tributos.history_type == '-':
            for campo in json.loads(log_entry.change_message)[0]['changed']['fields']:
                # { "campo": [previous, current], ...}
                alterados[campo] = (formatar_porcentagem(float(getattr(tributos.prev_record, campo)), "2"),
                                    formatar_porcentagem(float(getattr(tributos, campo)), "2"))

            log_list.append({'origem': tributos.get_origem_display(),
                             'destino': tributos.get_destino_display(),
                             'history_date': tributos.history_date.strftime("%d/%m/%Y %H:%M:%S"),
                             'usuario': User.objects.get(pk=tributos.history_user_id).username,
                             'alterados': alterados
                             })
    log['logs'] = log_list
    return log


MODELOS['subsTribut'] = _subs_tribut
