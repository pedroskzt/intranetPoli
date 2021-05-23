from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
phone_regex = RegexValidator(regex=r'^\(\d{2}\)\s\d{4}\-\d{4}$',
                             message="Telefone deve ser no formato: '(00) 0000-0000'.")

alphanumeric_regex = RegexValidator(regex='^[0-9A-Za-zÀ-ÖØ-öø-ÿ .]*$', message="Digite apenas Letras ou Números!")


class Assinatura(models.Model):
    nome = models.CharField(max_length=100, unique=True, validators=[alphanumeric_regex])
    departamento = models.CharField(max_length=100, validators=[alphanumeric_regex])
    fone = models.CharField(max_length=17, validators=[phone_regex])
    ramal = models.CharField(max_length=4)

    def __str__(self):
        return self.nome
