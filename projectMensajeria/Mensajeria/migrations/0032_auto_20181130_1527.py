# Generated by Django 2.0.7 on 2018-11-30 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0031_mensajeria_externa_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensajeria_externa',
            name='archivo',
            field=models.FileField(upload_to='media/acuse/'),
        ),
    ]