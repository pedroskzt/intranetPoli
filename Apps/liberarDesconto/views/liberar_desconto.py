from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render

from Apps.liberarDesconto.models.log import Log as LogDescontos
from intranetPoli.decorators import verificar_permissoes


def _get_empresas_e_descontos():
    with connection.cursor() as cursor:
        select = f"select POL_EMPRESA_INFO.parempr_id, " \
                 f"par_empresas.desc_sigla_empresa, " \
                 f"pol_empresa_info.perc_maxdesc " \
                 f"from pol_empresa_info, par_empresas " \
                 f"where pol_empresa_info.parempr_id = par_empresas.id " \
                 f"order by par_empresas.desc_sigla_empresa;"
        cursor.execute(select)
        desconto_filiais = cursor.fetchall()
        return [{'id': desconto_filial[0],
                 'filial': desconto_filial[1],
                 'desconto': float(desconto_filial[2]),
                 'status': '' if desconto_filial[2] == 26 else 'Liberado'}
                for desconto_filial in desconto_filiais] if desconto_filiais else False


def _update_descontos(desconto_filiais):
    with connection.cursor() as cursor:
        for desconto in desconto_filiais:
            update = f"update DR.pol_empresa_info " \
                     f"set PERC_MAXDESC = {desconto_filiais[desconto]} " \
                     f"WHERE PAREMPR_ID = {desconto} AND PERC_MAXDESC <> {desconto_filiais[desconto]};"
            cursor.execute(update)


def _log_update_desconto(desconto_filiais_anterior, desconto_filiais_novo):
    for desconto_filial in desconto_filiais_anterior:
        if f"{desconto_filial['desconto']:.2f}" != desconto_filiais_novo[desconto_filial['id']]:
            LogDescontos.objects.create(usuario=User.objects.get())

@login_required
@verificar_permissoes(permissoes_exigidas=['controleAcesso.pode_liberar_desconto'])
def liberar_desconto(request):
    contexto = {'desconto_filiais': _get_empresas_e_descontos()}
    if request.method == 'POST':
        novos_descontos_filiais = {}
        for filial in request.POST:
            if 'csrf' in filial:
                continue
            else:
                novos_descontos_filiais[int(filial.split('_')[1])] = request.POST[filial].replace(',', '.')
        try:
            _update_descontos(novos_descontos_filiais)
        except Exception as err:
            msg_erro = ''

            for desconto_filial in contexto['desconto_filiais']:
                # Testa se houve alteração no valor do desconto para cada filial. Caso haja alteração, imprime na
                # mensagem de erro.
                if f"{desconto_filial['desconto']:.2f}" != novos_descontos_filiais[desconto_filial['id']]:
                    msg_erro += f'<li>{desconto_filial["filial"]} -> {novos_descontos_filiais[desconto_filial["id"]]}</li>'
            msg_erro += f'<li>Erro: {err}</li>'
            messages.error(request, f"Falha ao alterar os descontos<ul>{msg_erro}</ul", extra_tags='safe')
        else:
            for desconto_filial in contexto['desconto_filiais']:
                # Testa se houve alteração no valor do desconto para cada filial. Casp haja alteração, registra no LOG.
                if f"{desconto_filial['desconto']:.2f}" != novos_descontos_filiais[desconto_filial['id']]:
                    LogDescontos.objects.create(usuario=request.user,
                                                id_linha_alterada=desconto_filial['id'],
                                                valor_anterior=desconto_filial['desconto'],
                                                novo_valor=novos_descontos_filiais[desconto_filial['id']])
            contexto['desconto_filiais'] = _get_empresas_e_descontos()
            messages.success(request, f'Valores alterados com sucesso.')
    return render(request, 'liberarDesconto/liberar_desconto.html', context=contexto)
