# Generated by Django 4.2.2 on 2023-07-08 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reactivos', '0002_alter_reactivo_consecutivo_ingreso'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumo',
            name='cantidad',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
