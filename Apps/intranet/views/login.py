from django.contrib.auth.models import auth, User
from django.shortcuts import redirect, render


def _campo_vazio(campo):
    return not campo.strip()


def login(request):
    """
    Inicia uma sessão com os dados do usuário.
    :param request:
    :return:
    """
    contexto = {'validacao': {'form_error': False,
                              'usuario': {'tag': '', 'mensagem': 'Campo Usuário não pode ser vazio.'},
                              'senha': {'tag': '', 'mensagem': 'Campo Senha não pode ser vazio'}}}
    if request.method == 'POST':
        redirecionamento = request.POST.get('next')
        usuario = request.POST['usuario']
        senha = request.POST['senha']

        if _campo_vazio(usuario):
            contexto['validacao']['form_error'] = True
            contexto['validacao']['usuario']['tag'] = 'is-invalid'

        if _campo_vazio(senha):
            print('senha invalido')
            contexto['validacao']['form_error'] = True
            contexto['validacao']['senha']['tag'] = 'is-invalid'

        if contexto['validacao']['form_error'] is False:
            if User.objects.filter(username=usuario).exists():
                nome = User.objects.filter(username=usuario).values_list('username', flat=True).get()
                user = auth.authenticate(request, username=nome, password=senha)
                if user is not None:
                    auth.login(request, user)
                    if redirecionamento:
                        return redirect(redirecionamento)
                    else:
                        return redirect('pagina_inicial')
            else:
                contexto['validacao']['form_error'] = True
                contexto['validacao']['usuario']['tag'] = 'is-invalid'
                contexto['validacao']['usuario']['mensagem'] = 'Usuário ou Senha incorretos.'

        contexto['form'] = {'usuario': usuario}
    return render(request, 'intranet/index.html', context=contexto)


def logout(request):
    """
    Encerra a sessão.
    :param request:
    :return:
    """
    redirecionamento = request.POST.get('next')
    auth.logout(request)
    if redirecionamento:
        return redirect(redirecionamento)
    else:
        return redirect('pagina_inicial')
