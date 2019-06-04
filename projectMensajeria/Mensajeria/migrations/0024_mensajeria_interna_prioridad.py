# Generated by Django 2.0.7 on 2018-10-31 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0023_mensajeria_interna_comentario'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensajeria_interna',
            name='prioridad',
            field=models.CharField(choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta')], default='Baja', max_length=5),
            preserve_default=False,
        ),
    ]
