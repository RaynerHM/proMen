# Generated by Django 2.0.7 on 2018-09-01 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mensajeria', '0014_auto_20180901_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('ver', 'Puede ver'), ('crear', 'Puede crear'), ('eliminar', 'Puede Eliminar')),
            },
        ),
    ]