# Generated by Django 3.1.7 on 2021-07-22 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flair', '0022_auto_20210722_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flairtype',
            name='flair_type',
            field=models.CharField(choices=[('default', 'Default'), ('award', 'Award'), ('temporary', 'Temporary')], default='default', max_length=255, verbose_name='Flairs Type'),
        ),
    ]