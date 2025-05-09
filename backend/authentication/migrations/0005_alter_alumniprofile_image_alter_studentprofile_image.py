# Generated by Django 5.2 on 2025-04-11 19:53

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_alumniprofile_company_alter_alumniprofile_dept_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumniprofile',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, default='default_alumni', max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, default='default_ayh3h7', max_length=255, null=True, verbose_name='image'),
        ),
    ]
