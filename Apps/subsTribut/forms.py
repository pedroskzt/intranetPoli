from django import forms

from Apps.subsTribut.models.tributos import Tributos


class CalculoForms(forms.Form):
    ESTADOS = (
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'),
        ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    )
    CST_CHOICES = [('00', 'ICMS Normal'), ('10', 'ICMS ST')]

    origem = forms.ChoiceField(label='Origem', choices=ESTADOS)
    destino = forms.ChoiceField(label='Destino', choices=ESTADOS)

    # Nacionais
    quantidade_n = forms.IntegerField(label='Quantidade')
    valor_unitario_n = forms.FloatField(label='Valor Unitário')
    ipi_item_n = forms.FloatField(label='% IPI')

    # Importados
    quantidade_i = forms.IntegerField(label='Quantidade')
    valor_unitario_i = forms.FloatField(label='Valor Unitário')
    ipi_item_i = forms.FloatField(label='% IPI')

    valor_frete = forms.FloatField(label='Valor do Frete', help_text="Valor do Frete")
    valor_acessoria = forms.FloatField(label='Despesa Acessoria')

    cst = forms.ChoiceField(label='CST de Origem', choices=CST_CHOICES, widget=forms.RadioSelect(attrs={'class':'form-check-input'}))
    super_simples = forms.BooleanField(label='Super Simples', help_text="Cliente é Super Simples?")
    base_red = forms.BooleanField(label='Base Reduzida', help_text='Base de ICMS de Origem é reduzida?')
    consumidor_final = forms.BooleanField(label='Consumidor Final', help_text='Cliente é consumidor final?')
    estado_sp = forms.BooleanField(label='São Paulo', help_text='Venda dentro do estado de São Paulo?')
