from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connections
from django.db.utils import DatabaseError
from django.shortcuts import render, redirect

from Apps.resultadoContabil.forms.form_cadastro import FormConsultaCadastro
from intranetPoli.decorators import verificar_permissoes


def _query_cadastro(mes, ano):
    with connections['BI'].cursor() as cursor:
        cursor.execute(
            f'SELECT valr_irpj_prev, valr_csll_prev '
            f'FROM dw_resultado '
            f'WHERE numr_ano = {ano} '
            f'AND numr_mes = {mes} '
            f'AND indr_tipo = 1 '
            f'AND id_empresa = 1')
        retornoBanco = cursor.fetchone()
        colunas = [col[0] for col in cursor.description]
    return dict(zip(colunas, retornoBanco)) if retornoBanco else False


def _query_insert_cadastro(mes, ano, irpj, csll):
    with connections['BI'].cursor() as cursor:
        cursor.execute(f"INSERT INTO dw_resultado "
                       f"(numr_mes, numr_ano, indr_tipo, id_empresa, valr_irpj_prev, valr_csll_prev) "
                       f"VALUES "
                       f"({mes}, {ano}, 1, 1, {irpj}, {csll})")


def _query_update_cadastro(mes, ano, irpj, csll):
    with connections['BI'].cursor() as cursor:
        cursor.execute(f"UPDATE dw_resultado "
                       f"SET valr_irpj_prev = {irpj}, "
                       f"valr_csll_prev = {csll} "
                       f"WHERE numr_mes = {mes} "
                       f"AND numr_ano = {ano}"
                       f"AND id_empresa = 1"
                       f"AND indr_tipo = 1;")


def _query_recalcular_bi(mes, ano):
    with connections['BI'].cursor() as cursor:
        # cursor.execute(f"call dw_imp_ctb_prc({mes},{ano})")
        # cursor.callproc(f"dw_imp_ctb_prc", [mes, ano])
        pass


@login_required
@verificar_permissoes(permissoes_exigidas=['controleAcesso.pode_cadastrar_irpj'])
def index(request):
    form = FormConsultaCadastro()
    return render(request, 'resultadoContabil/index.html', context={'form': form})


@login_required
@verificar_permissoes(permissoes_exigidas=['controleAcesso.pode_cadastrar_irpj'])
def cadastro(request):
    contexto = {}
    if request.method == 'POST':
        form = FormConsultaCadastro(request.POST)
        contexto['form'] = form
        if 'consultar' in request.POST:
            cadastro = _query_cadastro(request.POST['mes'],
                                       request.POST['ano'])
            if cadastro is not False:
                if form.is_valid():
                    contexto['form'] = form
                    contexto['cadastro'] = cadastro
            else:
                messages.error(request, f"Cadastro de Previsão não encontrado, "
                                        f"preencha os campos IRPJ e CSLL"
                                        f" e salve um novo cadastro para {request.POST['mes']}/{request.POST['ano']}")
        else:
            mes = request.POST.get('mes')
            ano = request.POST.get('ano')
            irpj = request.POST.get('irpj')
            csll = request.POST.get('csll')
            if 'salvar' in request.POST:

                try:
                    _query_insert_cadastro(mes, ano, irpj, csll)
                except DatabaseError as error:
                    messages.error(request,
                                   f"Erro na inserção dos valores:"
                                   f"<ul><li>{mes}/{ano}</li>"
                                   f"<li>IRPJ: {irpj}</li>"
                                   f"<li>CSLL: {csll}</li>"
                                   f"<li>{error}</li></ul>",
                                   extra_tags='safe')
                else:
                    messages.success(request, "Valores cadastrados com Sucesso.")
                    return redirect('index_contabil')
            if 'atualizar' in request.POST:
                try:
                    _query_update_cadastro(mes, ano, irpj, csll)
                except DatabaseError as error:
                    messages.error(request,
                                   f"Erro na atualização dos valores:"
                                   f"<ul><li>{mes}/{ano}</li>"
                                   f"<li>IRPJ: {irpj}</li>"
                                   f"<li>CSLL: {csll}</li>"
                                   f"<li>{error}</li></ul>",
                                   extra_tags='safe')
                else:
                    messages.success(request, "Valores atualizados com Sucesso.")
                    return redirect('index_contabil')
    return render(request, 'resultadoContabil/index.html', context=contexto)


@login_required
@verificar_permissoes(permissoes_exigidas=['controleAcesso.pode_cadastrar_irpj'])
def recalcular(request):
    if request.method == 'POST':
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        try:
            _query_recalcular_bi(mes, ano)
        except DatabaseError as error:
            messages.error(request,
                           f"Erro no recalculo com a data:"
                           f"<ul><li>{mes}/{ano}</li>"
                           f"<li>{error}</li></ul>",
                           extra_tags='safe')
        else:
            messages.success(request, "Valores recalculados com Sucesso.")
    return redirect('index_contabil')
