# Generated by Django 3.1.7 on 2021-05-01 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flair', '0014_auto_20210502_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='flairtype',
            name='reddit_flair_template_id',
            field=models.CharField(blank=True, max_length=64, verbose_name="Reddit's Template ID to set if any"),
        ),
    ]
