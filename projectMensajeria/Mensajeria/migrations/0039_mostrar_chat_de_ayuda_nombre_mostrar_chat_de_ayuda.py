# Generated by Django 2.0.7 on 2019-01-31 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0038_mostrar_chat_de_ayuda'),
    ]

    operations = [
        migrations.AddField(
            model_name='mostrar_chat_de_ayuda',
            name='nombre_mostrar_chat_de_ayuda',
            field=models.CharField(choices=[('habilitar_mostrar_ayuda', 'Habilitar Mostrar Ayuda'), ('mostrar_ayuda', 'Mostrar Ayuda')], default='habilitar_mostrar_ayuda', max_length=25),
            preserve_default=False,
        ),
    ]
