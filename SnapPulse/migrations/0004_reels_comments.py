# Generated by Django 4.2.6 on 2023-11-15 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SnapPulse', '0003_post_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='reels',
            name='comments',
            field=models.ManyToManyField(to='SnapPulse.comments'),
        ),
    ]
