# Generated by Django 5.0 on 2023-12-23 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0003_mesured_places_permission_set_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='mesured_places',
            new_name='mesured_place',
        ),
    ]
