from django.db import models
from simple_history.models import HistoricalRecords


class Tributos(models.Model):
    class Meta:
        verbose_name = 'Tributo'
        verbose_name_plural = 'Tributos'

    ESTADOS = (
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'),
        ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    )
    origem = models.CharField(max_length=2, choices=ESTADOS)
    destino = models.CharField(max_length=2, choices=ESTADOS)
    mva = models.DecimalField(max_digits=19, decimal_places=4)
    mvaimp = models.DecimalField(max_digits=19, decimal_places=4)
    mvaaliq = models.DecimalField(max_digits=19, decimal_places=4)
    valr_fecop = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.get_origem_display()}/{self.get_destino_display()}'
