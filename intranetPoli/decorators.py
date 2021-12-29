from django.core.exceptions import PermissionDenied


def verificar_permissoes(permissoes_exigidas=[]):
    """
    Decorator para testar se o usuário tentando acessar a página ou realizar uma operação tem as permissões exigidas
    para acessar tal página ou tal operação.
    Caso possua, segue para a página.
    Caso não possua, direciona a pessoa para uma página de Acesso Negado (403)
    :param permissoes_exigidas: Lista de permissões exigidas para acessar tal página ou operação.
                                Formato: [<app_label>.<permission codename>,...]
    :return:
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists() and request.user.has_perms(permissoes_exigidas):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied(f'Permissões exigidas: {permissoes_exigidas}')

        return wrapper_func

    return decorator
