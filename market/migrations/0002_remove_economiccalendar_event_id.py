# Generated by Django 5.1.7 on 2025-03-26 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='economiccalendar',
            name='event_id',
        ),
    ]
