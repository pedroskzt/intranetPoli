from django.contrib.auth.models import User
from django.db import models


class Log(models.Model):
    """
    Modelo para registro de log das alterações realizadas no Banco DR sobre alteração de Desconto.
    Para consultar os logs, utilize o seguinte SQL:
    select
    ld.DATA_ALTERACAO ,
    ld.ID_LINHA_ALTERADA,
    pe.DESC_SIGLA_EMPRESA,
    ld.VALOR_ANTERIOR,
    ld.NOVO_VALOR,
    ld.USUARIO_ID,
    concat(concat(auth_user.first_name,' '), auth_user.last_name)
from liberardesconto_log ld, DR.par_empresas pe, auth_user
where ld.id_linha_alterada = pe.id AND auth_user.id = ld.usuario_id
order by ld.data_alteracao;
    """

    class Meta:
        verbose_name = "Log de Liberação de Desconto"
        verbose_name_plural = "Logs de Liberação de Desconto"

    usuario = models.ForeignKey(User, models.PROTECT)
    data_alteracao = models.DateTimeField(auto_now=True)
    id_linha_alterada = models.IntegerField()
    valor_anterior = models.DecimalField(max_digits=4, decimal_places=2)
    novo_valor = models.DecimalField(max_digits=4, decimal_places=2)
