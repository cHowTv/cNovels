# Generated by Django 3.2 on 2021-08-10 18:50

import django.core.validators
from django.db import migrations, models
import novel.models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0004_auto_20210810_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='bookImage',
            field=models.ImageField(blank=True, default='default_profile.jpg', null=True, upload_to='book/images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg']), novel.models.valid_image_mimetype, novel.models.valid_size]),
        ),
    ]
