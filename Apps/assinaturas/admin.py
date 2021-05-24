from django.contrib import admin
from Apps.assinaturas.models import Assinatura


# Register your models here.

class ListandoAssinaturas(admin.ModelAdmin):
    list_display = ('id', 'nome', 'departamento', 'fone', 'ramal')
    list_display_links = ('id', 'nome')
    search_fields = ('nome', 'ramal', 'departamento')


admin.site.register(Assinatura, ListandoAssinaturas)
