# Generated by Django 2.0.7 on 2018-10-30 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0022_mensajeria_interna_recibido_por'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensajeria_interna',
            name='comentario',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
