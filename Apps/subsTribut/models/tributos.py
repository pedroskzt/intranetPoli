from django.db import models


class Tributos(models.Model):
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
    mva = models.FloatField()
    mvaimp = models.FloatField()
    aliq = models.FloatField()
    mvaaliq = models.FloatField()
    basered = models.FloatField()
    ssimples = models.FloatField()
