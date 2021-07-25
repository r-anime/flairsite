# Generated by Django 3.1.7 on 2021-07-22 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flair', '0021_flairtype_wiki_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flairsawarded',
            name='flair_id',
            field=models.ForeignKey(limit_choices_to=models.Q(('flair_type', 'award'), ('flair_type', 'tiered-award'), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, to='flair.flairtype'),
        ),
        migrations.AlterField(
            model_name='flairtype',
            name='flair_type',
            field=models.CharField(choices=[('default', 'Default'), ('award', 'Award'), ('tiered-award', 'Tiered-Award'), ('temporary', 'Temporary')], default='default', max_length=255, verbose_name='Flairs Type'),
        ),
    ]