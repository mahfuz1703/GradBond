# Generated by Django 5.2 on 2025-04-11 19:53

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_events_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, default='default_cover', max_length=255, null=True, verbose_name='image'),
        ),
    ]
