from django import forms

from Apps.intranet.models.links import Links


def _campo_vazio(valor_campo, nome_campo, lista_de_erros):
    if not valor_campo.strip():
        lista_de_erros[nome_campo] = f'Este campo não pode estar vazio ou em branco.'


class NovoLinkForms(forms.ModelForm):
    class Meta:
        model = Links
        fields = ('titulo', 'descricao', 'logo', 'url')
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'logo': 'Logo',
            'url': 'Link da Página'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título'}),
            'url': forms.TextInput(attrs={'placeholder': 'Link da Página'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição'}),
        }


class AtualizaLinkForms(forms.ModelForm):
    class Meta:
        model = Links
        fields = ('id', 'titulo', 'descricao', 'logo', 'url', 'exibir', 'requer_acesso')
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'logo': 'Logo',
            'url': 'Link da Página',
            'exibir': 'Exibir?',
            'requer_acesso': 'Requer Acesso?'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título'}),
            'url': forms.TextInput(attrs={'placeholder': 'Link da Página'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição'})
        }
