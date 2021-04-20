from django import forms


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
    quantidade_n = forms.IntegerField(label='Quantidade',
                                      initial=1)
    valor_unitario_n = forms.DecimalField(label='Valor Unitário',
                                          max_digits=19,
                                          decimal_places=5)
    ipi_item_n = forms.DecimalField(label='% IPI',
                                    max_digits=19,
                                    decimal_places=5)
    base_red_n = forms.BooleanField(label='Base Reduzida',
                                  help_text='Base de ICMS de Origem é reduzida?',
                                  required=False)

    # Importados
    quantidade_i = forms.IntegerField(label='Quantidade',
                                      initial=1)
    valor_unitario_i = forms.DecimalField(label='Valor Unitário',
                                          max_digits=19,
                                          decimal_places=5)
    ipi_item_i = forms.DecimalField(label='% IPI',
                                    max_digits=19,
                                    decimal_places=5)

    base_red_i = forms.BooleanField(label='Base Reduzida',
                                  help_text='Base de ICMS de Origem é reduzida?',
                                  required=False)

    # Gerais
    valor_frete = forms.DecimalField(label='Valor do Frete',
                                     help_text="Valor do Frete",
                                     max_digits=19,
                                     decimal_places=5)
    valor_acessoria = forms.DecimalField(label='Despesa Acessoria',
                                         max_digits=19,
                                         decimal_places=5)

    # cst = forms.ChoiceField(label='CST de Origem',
    #                         help_text='ICMS Normal (Não Calcula ST) ICMS ST (Calcula Base e Valor ST)',
    #                         choices=CST_CHOICES,
    #                         widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    super_simples = forms.BooleanField(label='Super Simples',
                                       help_text="Cliente é Super Simples?",
                                       required=False)
    consumidor_final = forms.BooleanField(label='Consumidor Final',
                                          help_text='Cliente é consumidor final?',
                                          required=False)
    estado_sp = forms.BooleanField(label='São Paulo',
                                   help_text='Venda dentro do estado de São Paulo?',
                                   required=False)
