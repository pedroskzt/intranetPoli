from django.contrib import admin
from django.contrib.auth.models import User, Group
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


class MyAdminSite(admin.AdminSite):
    def __init__(self):
        admin.AdminSite.__init__(self)
    login_template = 'intranet/login.html'

admin.site = MyAdminSite()
admin.site.register(Links, ListandoLinks)
admin.site.register(User)
admin.site.register(Group)
