from django import forms

from Apps.intranet.models.links import Links


class NovoLinkForms(forms.ModelForm):
    class Meta:
        model = Links
        fields = ('titulo', 'descricao', 'logo', 'url', 'exibir', 'requer_acesso', 'intranet')
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'logo': 'Logo',
            'url': 'Link da Página',
            'exibir': 'Exibir?',
            'requer_acesso': 'Requer Acesso?',
            'intranet': 'Intranet?'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título'}),
            'url': forms.TextInput(attrs={'placeholder': 'Link da Página'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição'}),
        }


class AtualizaLinkForms(forms.ModelForm):
    class Meta:
        model = Links
        fields = ('id', 'titulo', 'descricao', 'logo', 'url', 'exibir', 'requer_acesso', 'intranet')
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'logo': 'Logo',
            'url': 'Link da Página',
            'exibir': 'Exibir?',
            'requer_acesso': 'Requer Acesso?',
            'intranet': 'Intranet?'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título'}),
            'url': forms.TextInput(attrs={'placeholder': 'Link da Página'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição'})
        }
