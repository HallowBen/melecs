# Generated by Django 5.0 on 2023-12-23 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0009_alter_mesurement_data_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesurement_data',
            name='Place',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_side.mesured_place'),
        ),
    ]