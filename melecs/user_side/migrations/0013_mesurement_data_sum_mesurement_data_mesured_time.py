# Generated by Django 5.0 on 2023-12-24 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0012_all_mesurement'),
    ]

    operations = [
        migrations.AddField(
            model_name='mesurement_data',
            name='SUM',
            field=models.IntegerField(blank=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mesurement_data',
            name='mesured_time',
            field=models.IntegerField(blank=True, default=0, editable=False),
            preserve_default=False,
        ),
    ]
