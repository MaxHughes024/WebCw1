# Generated by Django 5.0.3 on 2024-03-26 21:41

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_remove_story_name_alter_author_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='myApp.author'),
        ),
        migrations.AddField(
            model_name='story',
            name='date',
            field=models.DateField(default=datetime.date(2024, 3, 26)),
        ),
        migrations.AddField(
            model_name='story',
            name='details',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='story',
            name='region',
            field=models.CharField(default=None, max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='story',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
