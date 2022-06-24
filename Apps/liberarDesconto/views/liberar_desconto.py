from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, redirect

from Apps.liberarDesconto.models.log import Log as LogDescontos
from Apps.liberarDesconto.models.usuarios_autorizacao import Usuarios_autorizacao
from intranetPoli.decorators import verificar_permissoes


def _get_empresas_e_descontos():
    with connection.cursor() as cursor:
        select = f"SELECT POL_EMPRESA_INFO.PAREMPR_ID, " \
                 f"PAR_EMPRESAS.DESC_SIGLA_EMPRESA, " \
                 f"POL_EMPRESA_INFO.PERC_MAXDESC " \
                 f"FROM DR.POL_EMPRESA_INFO, DR.PAR_EMPRESAS " \
                 f"WHERE POL_EMPRESA_INFO.PAREMPR_ID = PAR_EMPRESAS.id " \
                 f"ORDER BY PAR_EMPRESAS.DESC_SIGLA_EMPRESA;"
        cursor.execute(select)
        desconto_filiais = cursor.fetchall()
        return [{'id_linha_alterada': desconto_filial[0],
                 'filial': desconto_filial[1],
                 'desconto': float(desconto_filial[2])}
                for desconto_filial in desconto_filiais] if desconto_filiais else False


def _update_descontos(desconto_filiais):
    with connection.cursor() as cursor:
        for desconto in desconto_filiais:
            update = f"UPDATE DR.POL_EMPRESA_INFO " \
                     f"SET PERC_MAXDESC = {desconto_filiais[desconto]} " \
                     f"WHERE PAREMPR_ID = {desconto} AND PERC_MAXDESC <> {desconto_filiais[desconto]};"
            cursor.execute(update)


def _log_update_desconto(desconto_filiais_anterior, desconto_filiais_novo, usuarios_autorizacao, usuario):
    for desconto_filial in desconto_filiais_anterior:
        # Testa se houve alteração no valor do desconto para cada filial. Caso haja alteração, registra no LOG.
        if float(f"{desconto_filial['desconto']:.2f}") != float(
                desconto_filiais_novo[desconto_filial['id_linha_alterada']]):
            LogDescontos.objects.create(alterado_por=usuario,
                                        autorizado_por=usuarios_autorizacao[desconto_filial['id_linha_alterada']],
                                        id_linha_alterada=desconto_filial['id_linha_alterada'],
                                        valor_anterior=desconto_filial['desconto'],
                                        novo_valor=desconto_filiais_novo[desconto_filial['id_linha_alterada']])
            # data_alteracao=Now())


def _get_nome_filiais():
    with connection.cursor() as cursor:
        select = f'SELECT ID, DESC_SIGLA_EMPRESA FROM DR.PAR_EMPRESAS;'
        cursor.execute(select)
        return dict(cursor.fetchall())


def _identificar_alteracao(desconto_filiais_anterior, desconto_filiais_novo):
    alteracoes = []
    for desconto_filial in desconto_filiais_anterior:
        if float(f"{desconto_filial['desconto']:.2f}") != float(
                desconto_filiais_novo[desconto_filial['id_linha_alterada']]):
            alteracoes.append(desconto_filial)
    return alteracoes


def _get_padrao_desconto():
    with connection.cursor() as cursor:
        select = f"SELECT POL_EMPRESA_INFO.PAREMPR_ID, " \
                 f"POL_EMPRESA_INFO.PERC_PADRAO, " \
                 f"POL_EMPRESA_INFO.PERC_MAXIMO, " \
                 f"PAR_EMPRESAS.DESC_SIGLA_EMPRESA " \
                 f"FROM DR.POL_EMPRESA_INFO, DR.PAR_EMPRESAS " \
                 f"WHERE POL_EMPRESA_INFO.PAREMPR_ID = PAR_EMPRESAS.ID " \
                 f"ORDER BY PAR_EMPRESAS.DESC_SIGLA_EMPRESA;"
        cursor.execute(select)
        desconto_filiais = cursor.fetchall()
        return ({desconto_filial[0]: float(desconto_filial[1])   # Valor do desconto padrão por loja
                 for desconto_filial in desconto_filiais},
                {desconto_filial[0]: float(desconto_filial[2])   # Valor do desconto MÁXIMO por loja
                 for desconto_filial in desconto_filiais}) if desconto_filiais else (False, False)


@login_required
@verificar_permissoes(permissoes_exigidas=['controleAcesso.pode_liberar_desconto'])
def liberar_desconto(request):
    usuarios_autorizacao = Usuarios_autorizacao.objects.all().values_list('id', 'nome_usuario', 'pode_autorizar')
    contexto = {"title": 'Liberar Desconto',
                'desconto_filiais': _get_empresas_e_descontos(),
                'autorizado_por': [{'id_usuario': id_usuario,
                                    'nome': nome,
                                    'pode_autorizar': pode_autorizar} for id_usuario, nome, pode_autorizar in
                                   usuarios_autorizacao]}

    nome_filiais = _get_nome_filiais()
    if request.method == 'POST':
        novos_descontos_filiais = {}
        novos_usuarios_autorizacao = {}

        houve_erro = False
        mensagem_erro = ''
        padroes, limite = _get_padrao_desconto()

        for filial in request.POST:
            if 'csrf' in filial or 'voltar_padrao_desconto' in filial:
                continue
            else:
                if 'desconto' in filial:
                    linha = int(filial.split('_')[1])
                    if "voltar_padrao_desconto" in request.POST:
                        novos_descontos_filiais[linha] = padroes[linha]
                    else:
                        desconto = request.POST[filial].replace(',', '.')
                        if float(desconto) > limite[linha]:
                            houve_erro = True
                            mensagem_erro += f'<li>{nome_filiais[linha]}' \
                                             f' -> Desconto ({desconto}%) maior que o limite permitido para esta ' \
                                             f'filial ({limite[linha]}%) '
                        novos_descontos_filiais[linha] = desconto
                if 'autorizado' in filial:
                    if int(request.POST[filial]) == -1:
                        # Testa se em alguma linha, faltou selecionar o usúario que autorizou o desconto.2.
                        # Se houver, gera mensagem de erro para esta linha
                        mensagem_erro += f'<li>{nome_filiais[int(filial.split("_")[1])]}' \
                                         f' -> Selecionar o usuário que autorizou</li>'
                        houve_erro = True
                    else:
                        linha = int(filial.split('_')[1])
                        if "voltar_padrao_desconto" in request.POST:
                            novos_usuarios_autorizacao[linha] = Usuarios_autorizacao.objects.get(
                                nome_usuario='CPD')
                        else:
                            novos_usuarios_autorizacao[linha] = Usuarios_autorizacao.objects.get(
                                pk=int(request.POST[filial]))
        alteracoes = _identificar_alteracao(contexto['desconto_filiais'], novos_descontos_filiais)
        if alteracoes:
            if houve_erro is False:
                try:
                    _update_descontos(novos_descontos_filiais)
                except Exception as err:
                    msg_erro = ''
                    for desconto_filial in alteracoes:
                        # Insere mensagem de erro para cada linha alterada que contenha algum erro.
                        msg_erro += f'<li>{nome_filiais[int(desconto_filial["filial"].split("_")[1])]} -> ' \
                                    f'{desconto_filial["filial"]} ' \
                                    f':: {novos_descontos_filiais[desconto_filial["id"]]}</li>'
                    msg_erro += f'<li>Erro: {err}</li>'
                    messages.error(request, f"Falha ao alterar os descontos<ul>{msg_erro}</ul", extra_tags='safe')
                else:
                    _log_update_desconto(alteracoes, novos_descontos_filiais,
                                         novos_usuarios_autorizacao,
                                         request.user)
                    contexto['desconto_filiais'] = _get_empresas_e_descontos()
                    messages.success(request, f'Valores alterados com sucesso.')
            else:
                messages.error(request, f"Falha ao alterar os descontos<ul>{mensagem_erro}</ul", extra_tags='safe')
        else:
            mensagem_erro = f"Nenhum desconto com valor diferente do padrão " \
                            f"({contexto['padrao']['valor_desconto_padrao']}%) foi digitado!"
            messages.error(request, mensagem_erro, extra_tags='safe')
    for filial in contexto['desconto_filiais']:
        filial['alterado_por'] = 'PL/SQL'
        filial['data_alteracao'] = '-'
        filial['autorizado_por'] = Usuarios_autorizacao.objects.get(nome_usuario='CPD').pk
        log = LogDescontos.objects.filter(id_linha_alterada=filial['id_linha_alterada'])
        if log:
            log = log.latest('data_alteracao')
            if filial['desconto'] == float(log.novo_valor):
                filial['alterado_por'] = log.alterado_por.get_full_name()
                filial['data_alteracao'] = log.data_alteracao
                filial['autorizado_por'] = log.autorizado_por.id
    return render(request, 'liberarDesconto/liberar_desconto.html', context=contexto)
