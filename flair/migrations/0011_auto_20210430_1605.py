# Generated by Django 3.1.7 on 2021-04-30 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flair', '0010_flairtype_reddit_flair_css'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flairtype',
            old_name='reddit_flair_css',
            new_name='reddit_flair_css_class',
        ),
    ]
