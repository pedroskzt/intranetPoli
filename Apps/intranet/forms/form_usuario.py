from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from django.core.exceptions import ValidationError

# class NovoUsuarioForms(forms.ModelForm):
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Senha'}),
#                                        label='Confirmar Senha')
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}), required=True, label='E-mail')
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'first_name', 'last_name', 'email', 'groups')
#         labels = {
#             'username': 'Usuário',
#             'password': 'Senha',
#             'first_name': 'Nome',
#             'last_name': 'Sobrenome',
#             'groups': 'Grupo de Acesso'
#         }
#         widgets = {
#             'username': forms.TextInput(attrs={'placeholder': 'Usuário'}),
#             'password': forms.PasswordInput(attrs={'placeholder': 'Senha'}),
#             'first_name': forms.TextInput(attrs={'placeholder': 'Nome'}),
#             'last_name': forms.TextInput(attrs={'placeholder': 'Sobrenome'}),
#             'groups': forms.Select(attrs={'required': 'true'})  # Mudar required também no HTML
#         }

GRUPOS = []
for grupo in Group.objects.all():
    GRUPOS.append((grupo.id, grupo))


class NovoUsuarioForms(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuário', 'autocomplete': 'username'}),
                              label='Usuário')
    nome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome'}), required=False, label='Nome')
    sobrenome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Sobrenome'}), required=False,
                                label='Sobrenome')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-mail', 'autocomplete': 'email'}),
                             label='E-mail')
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'autocomplete': 'new-password'}),
                            label='Senha',
                            help_text=password_validators_help_text_html())
    confirma_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Senha', 'autocomplete': 'new-password'}),
        label='Confirmar Senha')
    groups = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'placeholder': 'Grupo de Acesso'}),
                                       label='Grupo de Acesso',
                                       choices=GRUPOS)

    adm_intranet = forms.BooleanField(widget=forms.CheckboxInput(),
                                      required=False,
                                      initial=False,
                                      label='Administrador da Intranet')

    def clean(self):
        usuario = self.cleaned_data.get('usuario')
        email = self.cleaned_data.get('email')
        senha = self.cleaned_data.get('senha')
        confirma_senha = self.cleaned_data.get('confirma_senha')

        if User.objects.filter(username=usuario).exists() is True:
            self.add_error('usuario', 'Já existe uma conta com este usuário!')

        if User.objects.filter(email=email).exists() is True:
            self.add_error('email', 'Já existe uma conta com este email!')

        if senha != confirma_senha:
            self.add_error('confirma_senha', 'As senhas não coincidem!')
        elif senha is not None:
            try:
                validate_password(senha)
            except ValidationError as error:
                for erro in error:
                    self.add_error('senha', erro)
        return self.cleaned_data
