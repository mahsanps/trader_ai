# Generated by Django 5.1.7 on 2025-04-18 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='url',
            field=models.URLField(max_length=1000),
        ),
    ]
