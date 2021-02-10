from django.contrib import admin

from Apps.subsTribut.models.tributos import Tributos


# Register your models here.

class ListandoTributos(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin_changelists.css',)
        }

    list_display = ('id', 'origem', 'destino', 'mva', 'mvaimp', 'aliq', 'mvaaliq', 'basered', 'ssimples')
    list_editable = ('mva', 'mvaimp', 'aliq', 'mvaaliq', 'basered', 'ssimples')
    list_filter = ('origem',)
    ordering = ('origem', 'destino')


admin.site.register(Tributos, ListandoTributos)
