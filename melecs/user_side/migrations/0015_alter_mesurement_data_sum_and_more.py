# Generated by Django 5.0 on 2023-12-24 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0014_alter_all_mesurement_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesurement_data',
            name='SUM',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='mesurement_data',
            name='mesured_time',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]