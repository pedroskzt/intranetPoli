# Generated by Django 2.2 on 2021-05-06 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subsTribut', '0004_delete_tributos_constantes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tributos',
            name='aliq',
        ),
    ]