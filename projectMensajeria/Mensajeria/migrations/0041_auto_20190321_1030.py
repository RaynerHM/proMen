# Generated by Django 2.0.7 on 2019-03-21 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0040_auto_20190131_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensajeria_externa',
            name='destinatario',
            field=models.CharField(max_length=100),
        ),
    ]
