# Generated by Django 4.0 on 2022-03-09 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0015_alter_orders_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPlant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_plant', to='plants.plants')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_plant', to='plants.customuser')),
            ],
            options={
                'unique_together': {('user_id', 'plant_id')},
            },
        ),
    ]