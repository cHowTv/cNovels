# Generated by Django 3.2.7 on 2022-03-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0035_user_has_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weekly',
            name='audios_of_week',
            field=models.ManyToManyField(blank=True, related_name='weekaudios', to='novel.Audio'),
        ),
    ]
