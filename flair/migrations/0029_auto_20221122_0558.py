# Generated by Django 3.1.13 on 2022-11-22 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flair', '0028_auto_20210725_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='flairtype',
            name='display_image',
            field=models.ImageField(upload_to='flair_images', verbose_name='Image shown on server for flair'),
        ),
        migrations.AlterField(
            model_name='flairsawarded',
            name='flair_id',
            field=models.ForeignKey(limit_choices_to=models.Q(('flair_type', 'achievement'), ('flair_type', 'custom'), ('flair_type', 'tiered-award'), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, to='flair.flairtype'),
        ),
        migrations.AlterField(
            model_name='flairtype',
            name='flair_type',
            field=models.CharField(choices=[('general', 'General'), ('custom', 'Custom'), ('list', 'List'), ('achievement', 'Achievement'), ('temporary', 'Temporary'), ('override', 'Override')], default='default', max_length=255, verbose_name='Flairs Type'),
        ),
        migrations.AlterField(
            model_name='flairtype',
            name='reddit_flair_emoji',
            field=models.CharField(max_length=64, verbose_name='Emoji that will be added if selected'),
        ),
        migrations.AlterField(
            model_name='flairtype',
            name='wiki_display',
            field=models.BooleanField(default=False),
        ),
    ]
