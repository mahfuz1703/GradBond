# Generated by Django 5.1 on 2024-11-23 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_events_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='regLink',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
