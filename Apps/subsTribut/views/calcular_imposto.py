from django.contrib import messages
from django.db import connection
from django.shortcuts import render
from django.views import View

from Apps.subsTribut.forms import CalculoForms
from Apps.subsTribut.models import Tributos


# TODO: Adicionar alerta sobre valores serem apenas para referencia.

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
    template_name = 'subsTribut/form_calculo.html'
    model_class = Tributos

    def get(self, request):
        form = {'numr_negociacao': None}
        if _campo_vazio(request.GET.get('numr_negociacao')) is not True:
            form['numr_negociacao'] = request.GET.get('numr_negociacao')
            form['pol_intra_nego_vw'] = _get_pol_intra_nego_vw(form['numr_negociacao'])
            print(form['pol_intra_nego_vw'])
            if _negociacao_nao_encontrada(form['pol_intra_nego_vw']):
                messages.error(request, 'Número de negociação não encontrado. Verifique.')
                form['numr_negociacao'] = None
            else:
                form['pol_intra_item_nego_vw'] = _get_pol_intra_item_nego_vw(form['numr_negociacao'])
                self._calculo(form['pol_intra_nego_vw'], form['pol_intra_item_nego_vw'])
                messages.success(request, 'Negociação encontrada.')
        else:
            if request.GET:
                messages.error(request, 'Campo vazio, favor digitar o número da negociação.')
        contexto = {'form': form}

        return render(request, self.template_name, context=contexto)

    def post(self, request):
        form = self.form_class

        if form.is_valid():
            pass
            # form.save()
        contexto = {"form": form}

        return render(request, self.template_name, context=contexto)

    def _calculo(self, negociacao, itens):
        """
        Realiza o calculo do ST para cada item da negociação, e adiciona no dicionario de itens o valor
        de ST para cada ITEM. Também adiciona no dicionario de negociação, o valor total de ST da negociação.
        :param negociacao:
        :param itens:
        :return:
        """
        origem = negociacao['NOME_UF_EMPRESA']
        destino = negociacao['NOME_UF_CLIENTE']
        taxas = self.model_class.objects.get(origem=origem, destino=destino)
        negociacao['VALR_TOTAL_IMPOSTO'] = 0

        if taxas.mva != 0 and origem != destino:
            '''
            Condição: Se houver MVA e Origem for diferente do Destino.
            '''
            for item in itens:
                item['mva'] = float(taxas.mvaimp) if item['INDR_IMPORTADO'] else float(taxas.mva)
                item['aliquota_ICMS'] = float(item['PERC_ALIQ_ICMS'])
                item['aliquota_interna'] = float(taxas.mvaaliq)

                valor_item_bruto = float((item['VALR_ITEM'] - item['VALR_DESC_UNITARIO']) * item['QTDE_ITENS'])

                item['valor_base_ICMS'] = valor_item_bruto + float(item['VALR_FRETE']) + float(item['VALR_DESPESAS'])
                item['valor_ICMS'] = item['valor_base_ICMS'] * item['aliquota_ICMS']
                item['valor_base_ST'] = (item['valor_base_ICMS'] * item['mva']) + item['valor_base_ICMS']
                if negociacao['INDR_CONSUMIDOR_FINAL'] and negociacao['NUMR_INSC_ESTADUAL'] is None:
                    '''
                    Condição: Consumidor final e Não possui Inscrição Estadual
                    '''
                    item['valor_bruto_difal'] = item['valor_base_ICMS'] * item['aliquota_interna']
                    valor_difal = item['valor_bruto_difal'] - item['valor_ICMS']
                    item['VALR_IMPOSTO'] = valor_difal
                    negociacao['VALR_TOTAL_IMPOSTO'] += valor_difal
                elif negociacao['INDR_CONSUMIDOR_FINAL'] == 0:
                    '''
                    Condição: Não é Consumidor final
                    '''
                    item['valor_bruto_ST'] = item['valor_base_ST'] * item['aliquota_interna']
                    valor_ST = item['valor_bruto_ST'] - item['valor_ICMS']
                    item['VALR_IMPOSTO'] = valor_ST
                    negociacao['VALR_TOTAL_IMPOSTO'] += valor_ST
        else:
            negociacao['VALR_TOTAL_IMPOSTO'] = False
