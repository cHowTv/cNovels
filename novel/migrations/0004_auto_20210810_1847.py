# Generated by Django 3.2 on 2021-08-10 18:47

import django.core.validators
from django.db import migrations, models
import novel.models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0003_auto_20210810_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='story',
        ),
        migrations.AlterField(
            model_name='novel',
            name='bookFile',
            field=models.FileField(blank=True, upload_to='book_files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), novel.models.valid_pdf_mimetype, novel.models.valid_size]),
        ),
    ]