# Generated by Django 4.0 on 2022-02-16 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0009_plants_image_delete_plantimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plants',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]
