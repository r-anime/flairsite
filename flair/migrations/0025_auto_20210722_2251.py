# Generated by Django 3.1.7 on 2021-07-22 10:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flair', '0024_auto_20210722_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionlogging',
            name='action',
            field=models.CharField(max_length=256, verbose_name='Action attempted'),
        ),
        migrations.AlterField(
            model_name='actionlogging',
            name='action_info',
            field=models.CharField(max_length=256, verbose_name='Info related to the action'),
        ),
        migrations.AlterField(
            model_name='actionlogging',
            name='error',
            field=models.CharField(max_length=256, verbose_name='Error message'),
        ),
        migrations.AlterField(
            model_name='actionlogging',
            name='reddit_name',
            field=models.CharField(max_length=20, verbose_name='Redditor name'),
        ),
        migrations.AlterField(
            model_name='actionlogging',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp of event'),
        ),
        migrations.AlterField(
            model_name='actionlogging',
            name='user_agent',
            field=models.CharField(max_length=65536, null=True, verbose_name='The user-agent string from the user'),
        ),
        migrations.AlterField(
            model_name='flairsawarded',
            name='note',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='An optional note on why this was awarded'),
        ),
        migrations.AlterField(
            model_name='flairsawarded',
            name='override_reddit_flair_emoji',
            field=models.CharField(default='', max_length=16, verbose_name='Override Emoji'),
        ),
        migrations.AlterField(
            model_name='flairsawarded',
            name='override_static_image',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Server image path'),
        ),
        migrations.AlterField(
            model_name='flairtype',
            name='note',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='An optional note about this flair'),
        ),
        migrations.AlterField(
            model_name='flairtype',
            name='reddit_flair_emoji',
            field=models.CharField(max_length=16, verbose_name='Emoji that will be added if selected'),
        ),
        migrations.AlterField(
            model_name='flairtype',
            name='reddit_flair_text',
            field=models.CharField(blank=True, max_length=64, verbose_name='Text that will be added if selected'),
        ),
        migrations.AlterField(
            model_name='flairtype',
            name='static_image',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Server image path. Used by wiki page'),
        ),
        migrations.AlterField(
            model_name='flairtype',
            name='wiki_text',
            field=models.CharField(blank=True, default='', max_length=65536, verbose_name='Information displayed on the flair wiki page'),
        ),
        migrations.AlterField(
            model_name='flairtype',
            name='wiki_title',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Title of the flair displayed on the wiki'),
        ),
    ]
