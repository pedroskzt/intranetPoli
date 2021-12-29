from django.contrib import admin
from django.db import connection

from Apps.liberarDesconto.models.log import Log as LogDescontos
from Apps.liberarDesconto.models.usuarios_autorizacao import Usuarios_autorizacao


def _get_nome_filiais():
    with connection.cursor() as cursor:
        select = f'select id, desc_sigla_empresa from par_empresas;'
        cursor.execute(select)
        return dict(cursor.fetchall())


# Register your models here.
class ListandoLog(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nome_filiais = _get_nome_filiais()

    def nome_filial(self, log):
        return self.nome_filiais[log.id_linha_alterada]
    nome_filial.short_description = 'Filial'
    nome_filial.admin_order_field = 'log__id_linha_alterada'

    def get_usuario_full_name(self, log):
        return log.alterado_por.get_full_name()
    get_usuario_full_name.short_description = 'Alterado Por'
    get_usuario_full_name.admin_order_field = 'log__alterado_por'

    list_display = ('id', 'nome_filial', 'valor_anterior', 'novo_valor', 'get_usuario_full_name', 'autorizado_por', 'data_alteracao')
    ordering = ('-data_alteracao',)


class ListandoUsuariosAutorizados(admin.ModelAdmin):
    list_display = ('id', 'nome_usuario', 'pode_autorizar')
    list_display_links = ('nome_usuario',)
    list_editable = ('pode_autorizar',)
    ordering = ('-pode_autorizar', 'nome_usuario')


admin.site.register(LogDescontos, ListandoLog)
admin.site.register(Usuarios_autorizacao, ListandoUsuariosAutorizados)
