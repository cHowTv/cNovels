# Generated by Django 3.2.7 on 2021-11-21 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0019_auto_20211119_2225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='recently_viewed_novels',
        ),
        migrations.AddField(
            model_name='user',
            name='recently_viewed_chapters',
            field=models.ManyToManyField(blank=True, null=True, related_name='recently_viewed_chapters', to='novel.Chapters'),
        ),
        migrations.AlterField(
            model_name='chapters',
            name='novel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='novel.novel'),
        ),
    ]