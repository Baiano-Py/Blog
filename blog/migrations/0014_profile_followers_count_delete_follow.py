# Generated by Django 5.1.1 on 2024-09-24 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers_count',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
