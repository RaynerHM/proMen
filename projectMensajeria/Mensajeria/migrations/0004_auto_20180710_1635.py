# Generated by Django 2.0.7 on 2018-07-10 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0003_auto_20180710_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensajeria',
            name='fecha_entrega',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Entregada'),
        ),
    ]