# Generated by Django 2.0.7 on 2018-12-03 15:05

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0033_auto_20181130_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensajeria_externa',
            name='archivo',
            field=models.FileField(upload_to=django.core.files.storage.FileSystemStorage(location='/home/local/BELLBANK/rhernandez/Desktop/proyectos/pruebas/envMensajeria/projectMensajeria/static/media/acuse/')),
        ),
    ]