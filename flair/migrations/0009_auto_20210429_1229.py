# Generated by Django 3.1.7 on 2021-04-29 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flair', '0008_flairtype_flair_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
