# Generated by Django 3.1.7 on 2021-05-11 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flair', '0017_actionlogging'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionlogging',
            name='current_flair',
        ),
    ]
