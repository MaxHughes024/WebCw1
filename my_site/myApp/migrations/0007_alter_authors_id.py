# Generated by Django 5.0.3 on 2024-03-27 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0006_rename_author_authors_rename_story_stories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
