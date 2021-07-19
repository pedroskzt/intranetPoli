from django import forms
from django.core.validators import RegexValidator
from Apps.assinaturas.models import Assinatura

phone_regex = RegexValidator(regex=r'^\(\d{2}\)\s\d{4}\-\d{4}$',
                             message="Telefone deve ser no formato: '(00) 0000-0000'.")

alfanumerico_regex = RegexValidator(regex='^[0-9A-Za-zÀ-ÖØ-öø-ÿ .]*$', message="Digite apenas Letras ou Números!")


class AssinaturaForms(forms.ModelForm):
    class Meta:
        model = Assinatura
        fields = '__all__'
        labels = {'fone': 'Telefone'}
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'departamento': forms.TextInput(attrs={'placeholder': 'Departamento'}),
            'fone': forms.TextInput(attrs={'placeholder': 'Telefone'}),
            'ramal': forms.TextInput(attrs={'placeholder': 'Ramal'}),

        }
