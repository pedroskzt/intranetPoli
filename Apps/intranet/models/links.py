from django.contrib.auth.models import User
from django.db import models


class Links(models.Model):
    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
    titulo = models.CharField(max_length=30, unique=True)
    descricao = models.TextField(max_length=200)
    logo = models.ImageField(upload_to='logos')
    url = models.URLField(unique=True)
    exibir = models.BooleanField(default=False)
    requer_acesso = models.BooleanField(default=False)
    intranet = models.BooleanField(default=False)

    # Log de criação
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario_criacao = models.ForeignKey(User, related_name='usuario_criacao', on_delete=models.PROTECT)

    # Log de atualização
    data_ultima_alteracao = models.DateTimeField(auto_now=True)
    usuario_ultima_alteracao = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.titulo

