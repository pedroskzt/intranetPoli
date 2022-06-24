from django.contrib import messages
from django.db import connection
from django.shortcuts import render
from django.views import View

from Apps.subsTribut.forms import CalculoForms
from Apps.subsTribut.models import Tributos


def _campo_vazio(campo):
    """
    Valida se o Campo é vazio
    :param campo:
    :return: True se for vazio, False se não for vazio
    """
    return not campo or campo.strip()


def _negociacao_nao_encontrada(negociacao):
    """
    Valida se a negociação não existe
    :param negociacao:
    :return: True se não existir a negociação, False se existir.
    """
    return not negociacao


def _get_pol_intra_nego_vw(numr_negociacao):
    """
    Consulta o Banco de Dados e retorna um dicionario relacionando as colunas da View POL_INTRA_NEGO_VW com os
    respectivos valores de cada coluna.
    :param numr_negociacao:
    :return:
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM POL_INTRA_NEGO_VW WHERE NUMR_NEGOCIACAO={numr_negociacao}")
        retornoBanco = cursor.fetchone()
        colunas = [col[0] for col in cursor.description]
    return dict(zip(colunas, retornoBanco)) if retornoBanco else False


def _get_pol_intra_item_nego_vw(numr_negociacao):
    """
    Consulta o Banco de Dados e retorna um dicionario relacionando as colunas da View POL_INTRA_NEGO_VW com os
    respectivos valores de cada coluna.
    :param numr_negociacao:
    :return:
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM POL_INTRA_ITEM_NEGO_VW WHERE NUMR_NEGOCIACAO={numr_negociacao}")
        retornoBanco = cursor.fetchall()
        colunas = [col[0] for col in cursor.description]
    return [dict(zip(colunas, linha)) for linha in retornoBanco] if retornoBanco else False


class CalcularView(View):
    form_class = CalculoForms
    template_name = 'subsTribut/subsTribut.html'
    model_class = Tributos

    def get(self, request):
        contexto = {"title": 'ST',
                    'numr_negociacao': None}

        if _campo_vazio(request.GET.get('numr_negociacao')) is not True:
            contexto['numr_negociacao'] = request.GET.get('numr_negociacao')
            contexto['pol_intra_nego_vw'] = _get_pol_intra_nego_vw(contexto['numr_negociacao'])
            if _negociacao_nao_encontrada(contexto['pol_intra_nego_vw']):
                messages.error(request, 'Número de negociação não encontrado. Verifique.')
                contexto['numr_negociacao'] = None
            elif contexto['pol_intra_nego_vw']['NOME_UF_EMPRESA'] == 'DF':
                messages.error(request, 'Vendas com origem em Brasília, o imposto é calculado direto na nota!')
                contexto['numr_negociacao'] = None
            else:
                contexto['pol_intra_item_nego_vw'] = _get_pol_intra_item_nego_vw(contexto['numr_negociacao'])
                self._calculo(contexto['pol_intra_nego_vw'], contexto['pol_intra_item_nego_vw'])
                messages.success(request, 'Negociação encontrada.')
        else:
            if request.GET:
                messages.error(request, 'Campo vazio, favor digitar o número da negociação.')
        return render(request, self.template_name, context=contexto)

    def post(self, request):
        form = self.form_class

        if form.is_valid():
            pass
            # form.save()
        contexto = {"title": 'ST',
                    "form": form}

        return render(request, self.template_name, context=contexto)

    def _calculo(self, negociacao, itens):
        """
        Realiza o calculo do ST para cada item da negociação, e adiciona no dicionario de itens o valor
        de ST para cada ITEM. Também adiciona no dicionario de negociação, o valor total de ST da negociação.

        Condição: Consumidor final e Não Contribuinte
            Calculo: DIFAL
        Condição: Não é Consumidor final
            Calculo: ST

        :param negociacao:
        :param itens:
        :return:
        """
        origem = negociacao['NOME_UF_EMPRESA']
        destino = negociacao['NOME_UF_CLIENTE']
        taxas = self.model_class.objects.get(origem=origem, destino=destino)
        negociacao['VALR_TOTAL_IMPOSTO'] = 0
        negociacao['VALR_FECOP'] = float(taxas.valr_fecop)
        negociacao['FECOP'] = 0

        if origem != destino:
            '''
            Condição: Se houver MVA e Origem for diferente do Destino.
            '''
            for item in itens:
                item['mva'] = float(taxas.mvaimp) if item['INDR_IMPORTADO'] else float(taxas.mva)
                item['aliquota_ICMS'] = float(item['PERC_ALIQ_ICMS'])
                item['aliquota_interna'] = float(taxas.mvaaliq)

                item['valor_item_bruto'] = float((item['VALR_ITEM'] - item['VALR_DESC_UNITARIO']) * item['QTDE_ITENS'])
                item['valor_base_ICMS'] = item['valor_item_bruto'] + float(item['VALR_FRETE']) + float(
                    item['VALR_DESPESAS'])
                item['valor_ICMS'] = item['valor_base_ICMS'] * item['aliquota_ICMS']
                item['valor_base_ST'] = (item['valor_base_ICMS'] * item['mva']) + item['valor_base_ICMS']
                if negociacao['INDR_CONSUMIDOR_FINAL'] and negociacao['INDR_CONTRIBUINTE'] == 0:
                    '''
                    Condição: Consumidor final e Não Contribuinte
                    Calculo: DIFAL
                    '''

                    # difal_intermediario = item['valor_base_ICMS'] - item['valor_ICMS']
                    # difal_intermediario = difal_intermediario / (1 - item['aliquota_interna'])

                    # item['valor_bruto_difal'] = difal_intermediario * item['aliquota_interna']
                    # valor_difal = item['valor_bruto_difal'] - item['valor_ICMS']

                    # item['VALR_IMPOSTO'] = valor_difal
                    # negociacao['VALR_TOTAL_IMPOSTO'] += valor_difal

                    item['valor_bruto_difal'] = item['valor_base_ICMS'] * item['aliquota_interna']
                    item['VALR_IMPOSTO'] = (item['valor_bruto_difal'] - item['valor_ICMS'])
                    negociacao['VALR_TOTAL_IMPOSTO'] += item['VALR_IMPOSTO']
                    # for i in item:
                    #     print(f'{i}: {item[i]}')
                elif negociacao['INDR_CONSUMIDOR_FINAL'] == 0 and taxas.mva != 0:
                    '''
                    Condição: Não é Consumidor final
                    Calculo: ST
                    '''
                    item['valor_bruto_ST'] = item['valor_base_ST'] * item['aliquota_interna']
                    valor_ST = item['valor_bruto_ST'] - item['valor_ICMS']
                    item['VALR_IMPOSTO'] = valor_ST

                    negociacao['VALR_TOTAL_IMPOSTO'] += valor_ST
                    # for i in item:
                    #     print(f'{i}: {item[i]}')
        else:
            for item in itens:
                item['valor_item_bruto'] = float((item['VALR_ITEM'] - item['VALR_DESC_UNITARIO']) * item['QTDE_ITENS'])
            negociacao['VALR_TOTAL_IMPOSTO'] = False

        if taxas.valr_fecop > 0:
            """ Calcular o valor do imposto FECOP """
            for item in itens:
                item['aliquota_ICMS'] = float(item['PERC_ALIQ_ICMS'])
                item['valor_item_bruto'] = float((item['VALR_ITEM'] - item['VALR_DESC_UNITARIO']) * item['QTDE_ITENS'])
                item['valor_base_ICMS'] = item['valor_item_bruto'] + float(item['VALR_FRETE']) + float(
                    item['VALR_DESPESAS'])
                item['valor_ICMS'] = item['valor_base_ICMS'] * item['aliquota_ICMS']

                if negociacao['INDR_CONSUMIDOR_FINAL']:
                    fecop = item['valor_base_ICMS'] * float(taxas.valr_fecop)
                elif not negociacao['INDR_CONSUMIDOR_FINAL']:
                    if taxas.mva == 0:
                        fecop = item['valor_base_ICMS'] * float(taxas.valr_fecop)
                    else:
                        item['mva'] = float(taxas.mvaimp) if item['INDR_IMPORTADO'] else float(taxas.mva)
                        item['valor_base_ST'] = (item['valor_base_ICMS'] * item['mva']) + item['valor_base_ICMS']
                        fecop = item['valor_base_ST'] * float(taxas.valr_fecop)
                negociacao['FECOP'] += fecop

                if negociacao['VALR_TOTAL_IMPOSTO']:
                    negociacao['TOTAL'] = negociacao['FECOP'] + negociacao['VALR_TOTAL_IMPOSTO']
                else:
                    negociacao['TOTAL'] = False
