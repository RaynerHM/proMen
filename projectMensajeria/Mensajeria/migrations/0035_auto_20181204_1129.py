# Generated by Django 2.0.7 on 2018-12-04 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0034_auto_20181203_1105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mensajeria_externa',
            old_name='archivo',
            new_name='archivo_acuse',
        ),
    ]
