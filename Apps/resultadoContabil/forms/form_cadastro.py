from django import forms
from django.db import connections


def _query_cadastro(mes, ano):
    with connections['BI'].cursor() as cursor:
        cursor.execute(
            f'select t.valr_irpj_prev, t.valr_csll_prev '
            f'from dw_resultado t '
            f'where numr_ano = {ano} '
            f'and t.numr_mes = {mes} '
            f'and indr_tipo = 1 '
            f'and id_empresa = 1')
        retornoBanco = cursor.fetchone()
        colunas = [col[0] for col in cursor.description]
    return dict(zip(colunas, retornoBanco)) if retornoBanco else False


class FormConsultaCadastro(forms.Form):
    mes = forms.IntegerField(min_value=1,
                             max_value=12,
                             label='Mês',
                             widget=forms.NumberInput(attrs={'placeholder': 'Mês'}))

    ano = forms.IntegerField(min_value=1976,
                             max_value=9999,
                             label='Ano',
                             widget=forms.NumberInput(attrs={'placeholder': 'Ano'}))
