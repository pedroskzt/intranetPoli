from django.core.validators import RegexValidator
from django.db import models, connection

# Create your models here.
phone_regex = RegexValidator(regex=r'^\(\d{2}\)\s\d{4}\-\d{4}$',
                             message="Telefone deve ser no formato: '(00) 0000-0000'.")

alphanumeric_regex = RegexValidator(regex='^[0-9A-Za-zÀ-ÖØ-öø-ÿ .]*$', message="Digite apenas Letras ou Números!")


class Assinatura(models.Model):
    class Meta:
        verbose_name = 'Assinatura de Email'
        verbose_name_plural = 'Assinaturas de Email'
    CIDADES_CHOICES = []
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT CONCAT(parempr.desc_sigla_empresa, CONCAT(' - ', parempr.nome_uf_empresa)) from DR.par_empresas parempr, DR.par_entidades_vw parentd where parempr.numr_cgc_empresa = parentd.numr_cgc AND parentd.nome_razao_social LIKE 'POLIPECAS DIST%' order by parempr.desc_sigla_empresa;")
        CIDADES_CHOICES = [(empresa[0], empresa[0]) for empresa in cursor.fetchall()]

    codigo_usuario = models.IntegerField(unique=True, blank=True, null=True)
    nome = models.CharField(max_length=100, unique=True, validators=[alphanumeric_regex])
    departamento = models.CharField(max_length=100, validators=[alphanumeric_regex])
    fone = models.CharField(max_length=17, validators=[phone_regex])
    ramal = models.CharField(max_length=4)
    empresa = models.CharField(max_length=100, choices=CIDADES_CHOICES, default="")

    def __str__(self):
        return self.nome
