from django import forms
from django.core.validators import RegexValidator

from Apps.assinaturas.models import Assinatura

phone_regex = RegexValidator(regex=r'^\(\d{2}\)\s\d{4}\-\d{4}$',
                             message="Telefone deve ser no formato: '(00) 0000-0000'.")

alfanumerico_regex = RegexValidator(regex='^[0-9A-Za-zÀ-ÖØ-öø-ÿ .]*$', message="Digite apenas Letras ou Números!")


class CriaAssinaturaForms(forms.ModelForm):
    class Meta:
        model = Assinatura
        exclude = ('codigo_usuario',)
        labels = {'fone': 'Telefone',
                  'empresa': 'Empresa'}
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'departamento': forms.TextInput(attrs={'placeholder': 'Departamento'}),
            'fone': forms.TextInput(attrs={'placeholder': 'Telefone'}),
            'ramal': forms.TextInput(attrs={'placeholder': 'Ramal'}),
            'empresa': forms.Select(attrs={'class': 'form-select'})
        }

    def clean_nome(self):
        lista_minusculos = [' Da ', ' De ', ' Di ', ' Do ', ' Du ']
        nome = self.cleaned_data.get('nome').lower().title()
        for termo in lista_minusculos:
            nome = nome.replace(termo, termo.lower())
        return nome


class EditarAssinaturaForms(forms.ModelForm):
    class Meta:
        model = Assinatura
        exclude = ('codigo_usuario',)
        labels = {'fone': 'Telefone',
                  'empresa': 'Empresa'}
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'departamento': forms.TextInput(attrs={'placeholder': 'Departamento'}),
            'fone': forms.TextInput(attrs={'placeholder': 'Telefone'}),
            'ramal': forms.TextInput(attrs={'placeholder': 'Ramal'}),
            'empresa': forms.Select(attrs={'class': 'form-select'})
        }

        def clean_nome(self):
            lista_minusculos = [' Da ', ' De ', ' Di ', ' Do ', ' Du ']
            nome = self.cleaned_data.get('nome').lower().title()
            for termo in lista_minusculos:
                nome = nome.replace(termo, termo.lower())
            return nome
