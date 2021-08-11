# Generated by Django 3.2 on 2021-08-10 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0002_auto_20210803_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='chapter',
        ),
        migrations.AddField(
            model_name='chapters',
            name='novel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='novel.novel'),
        ),
    ]