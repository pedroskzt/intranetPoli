from django import forms

from Apps.catalogos.models import Catalogos


class NovoCatalogoForms(forms.ModelForm):
    class Meta:
        model = Catalogos
        fields = ('titulo', 'logo', 'url', 'exibir')
        labels = {
            'titulo': 'Título',
            'logo': 'Logo',
            'url': 'Link da Página',
            'exibir': 'Exibir?',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título'}),
            'url': forms.TextInput(attrs={'placeholder': 'Link do Catálogo'}),
        }


class AtualizaCatalogoForms(forms.ModelForm):
    class Meta:
        model = Catalogos
        fields = ('id', 'titulo', 'logo', 'url', 'exibir')
        labels = {
            'titulo': 'Título',
            'logo': 'Logo',
            'url': 'Link da Página',
            'exibir': 'Exibir?',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título'}),
            'url': forms.TextInput(attrs={'placeholder': 'Link do Catálogo'}),
        }
