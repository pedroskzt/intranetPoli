from django import forms


class FormConsultaCadastro(forms.Form):
    mes = forms.IntegerField(min_value=1,
                             max_value=12,
                             label='Mês',
                             widget=forms.NumberInput(attrs={'placeholder': 'Mês'}))

    ano = forms.IntegerField(min_value=1976,
                             max_value=9999,
                             label='Ano',
                             widget=forms.NumberInput(attrs={'placeholder': 'Ano'}))
