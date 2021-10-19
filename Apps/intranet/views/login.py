from django.contrib.auth.models import auth, User
from django.shortcuts import redirect, render
from django.urls import resolve


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
                              'senha': {'tag': '', 'mensagem': 'Campo Senha não pode ser vazio'}},
                'next': request.GET.get('next')}

    if request.method == 'POST':
        redirecionamento = request.POST.get('next')
        if resolve(redirecionamento).url_name == 'login' or resolve(redirecionamento).url_name == 'logout':
            redirecionamento = '/'
        contexto['next'] = redirecionamento
        usuario = request.POST['usuario']
        senha = request.POST['senha']

        if 'voltar-btn' in request.POST:
            if request.user.is_authenticated:
                return redirect(redirecionamento) if redirecionamento else redirect('pagina_inicial')
            else:
                return redirect('pagina_inicial')

        if _campo_vazio(usuario):
            contexto['validacao']['form_error'] = True
            contexto['validacao']['usuario']['tag'] = 'is-invalid'

        if _campo_vazio(senha):
            contexto['validacao']['form_error'] = True
            contexto['validacao']['senha']['tag'] = 'is-invalid'

        if contexto['validacao']['form_error'] is False:
            if User.objects.filter(username=usuario).exists():
                nome = User.objects.filter(username=usuario).values_list('username', flat=True).get()
                user = auth.authenticate(request, username=nome, password=senha)
                if user is not None:
                    auth.login(request, user)
                    return redirect(redirecionamento) if redirecionamento else redirect('pagina_inicial')

            contexto['validacao']['form_error'] = True
            contexto['validacao']['usuario']['tag'] = 'is-invalid'
            contexto['validacao']['usuario']['mensagem'] = 'Usuário ou Senha incorretos.'

        contexto['form'] = {'usuario': usuario}

    return render(request, 'intranet/login.html', context=contexto)


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
