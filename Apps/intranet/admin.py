from django.contrib import admin

from Apps.intranet.models.links import Links


# Register your models here.

class ListandoLinks(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('subsTribut/css/admin_changelists.css',)
        }

    list_display = ('titulo', 'url', 'data_ultima_alteracao',
                    'usuario_ultima_alteracao', 'exibir', 'requer_acesso')
    list_editable = ('exibir', 'requer_acesso')
    readonly_fields = ('usuario_criacao', 'usuario_ultima_alteracao')


admin.site.register(Links, ListandoLinks)
