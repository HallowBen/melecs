# Generated by Django 5.0 on 2023-12-26 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0017_archive_file_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archive',
            name='File_location',
        ),
        migrations.AlterField(
            model_name='archive',
            name='File',
            field=models.FileField(upload_to=models.CharField(max_length=20)),
        ),
    ]
