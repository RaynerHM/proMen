# Generated by Django 2.0.7 on 2018-08-17 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0010_auto_20180809_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensajeria',
            name='codigo',
            field=models.CharField(default='men00', max_length=30, verbose_name='Codigo de Mensajeria'),
            preserve_default=False,
        ),
    ]
