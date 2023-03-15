# Generated by Django 4.1.7 on 2023-03-15 11:13

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.fields
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email_confirmed', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='')),
                ('last_searched', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('has_interest', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserIntrest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobbies', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Traveling'), (2, 'Reading'), (3, 'Singing'), (4, 'Dancing'), (5, 'Movies')], max_length=255)),
                ('genre', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Action'), (2, 'Adventure'), (3, 'Comedy'), (4, 'Romance'), (5, 'Fantasy')], max_length=255)),
                ('profile', multiselectfield.db.fields.MultiSelectField(choices=[('Author', 'Author'), ('Reader', 'Reader')], max_length=255)),
                ('language', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Spanish'), (2, 'English'), (3, 'Yoruba')], max_length=255)),
                ('history', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Medieval'), (2, 'Cyberpunk'), (3, 'Iceage'), (4, 'Ile-ife dynasty'), (5, 'Neolitic'), (6, 'Northern Caliphate'), (7, 'Paleolithic')], max_length=255)),
                ('identity', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Women'), (2, 'Men'), (3, 'GenZ'), (4, 'Ile-ife dynasty'), (5, 'Neolitic'), (6, 'Northern Caliphate'), (7, 'Paleolithic')], max_length=255)),
                ('faith', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Christain'), (2, 'Muslim'), (3, 'Judaism'), (4, 'Ile-ife dynasty'), (5, 'Neolitic'), (6, 'Northern Caliphate'), (7, 'Paleolithic')], max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.fields.CharField, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
