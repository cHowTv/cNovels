# Generated by Django 3.2.7 on 2021-11-21 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0021_auto_20211121_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='state',
        ),
    ]