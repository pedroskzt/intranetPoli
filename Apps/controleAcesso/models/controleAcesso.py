from django.db import models


# Create your models here.
class ControleAcesso(models.Model):
    class Meta:
        managed = False  # No database table creation or deletion  \
        # operations will be performed for this model.

        # default_permissions = ()  # disable "add", "change", "delete"
        # # and "view" default permissions

        verbose_name = 'Controle de Acesso'
        verbose_name_plural = 'Controle de Acessos'

        permissions = [('pode_cadastrar_irpj', 'Pode Cadastrar IRPJ'),
                       ('pode_liberar_desconto', 'Pode Liberar Desconto'),
                       ('pode_acessar_painel_admin', 'Pode Acessar Painel de Admin')]
