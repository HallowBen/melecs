# Generated by Django 5.0 on 2023-12-22 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='mesurement_list',
            fields=[
                ('ID', models.SlugField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('Date', models.DateField(auto_now=True)),
            ],
        ),
    ]