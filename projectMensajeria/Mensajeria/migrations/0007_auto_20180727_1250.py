# Generated by Django 2.0.7 on 2018-07-27 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0006_auto_20180727_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensajeria',
            name='fecha_entrega',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha Entregado'),
        ),
    ]
