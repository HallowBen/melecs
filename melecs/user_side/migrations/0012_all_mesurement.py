# Generated by Django 5.0 on 2023-12-24 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0011_alter_mesurement_data_person_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='all_mesurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.IntegerField(default=0)),
                ('time', models.TimeField(auto_now=True)),
                ('ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_side.mesurement_list')),
            ],
        ),
    ]