# Generated by Django 2.0.7 on 2019-01-31 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0039_mostrar_chat_de_ayuda_nombre_mostrar_chat_de_ayuda'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('habilitar', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Mostrar_chat_de_ayuda',
        ),
    ]
