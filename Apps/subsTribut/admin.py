from django.contrib import admin

from Apps.subsTribut.models.tributos import Tributos


# Register your models here.

class ListandoTributos(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('subsTribut/css/admin_changelists.css',)
        }

    list_display = (
        'id', 'origem', 'destino', 'mva', 'mvaimp', 'mvaaliq', 'valr_fecop')
    list_editable = ('mva', 'mvaimp', 'mvaaliq', 'valr_fecop')
    list_filter = ('origem', 'destino')
    ordering = ('origem', 'destino')


admin.site.register(Tributos, ListandoTributos)
