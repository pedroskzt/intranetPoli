from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

from Apps.intranet.forms.form_usuario import NovoUsuarioForms


def adicionar_usuario(request):
    form = NovoUsuarioForms()
    if request.method == 'POST':
        form = NovoUsuarioForms(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username=form.cleaned_data['usuario'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['senha'],
                                                first_name=form.cleaned_data.get('nome'),
                                                last_name=form.cleaned_data.get('sobrenome'))
            new_user.is_staff = form.cleaned_data['adm_intranet']
            new_user.groups.set(Group.objects.filter(pk__in=form.cleaned_data['groups']))
            new_user.save()
            return redirect('painel_intranet')

    return render(request, 'intranet/painel/adicionar_usuario.html', context={'form': form})
