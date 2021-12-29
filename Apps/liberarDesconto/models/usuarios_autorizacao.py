from django.db import models


class Usuarios_autorizacao(models.Model):
    class Meta:
        db_table = 'liberardesconto_usuarios_auth'
        verbose_name = "Usuário Autorização"
        verbose_name_plural = "Usuários Autorização"

    nome_usuario = models.CharField(max_length=100)
    pode_autorizar = models.BooleanField()

    def __str__(self):
        return self.nome_usuario
