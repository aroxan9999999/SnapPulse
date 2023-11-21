# Generated by Django 4.2.6 on 2023-11-14 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('direct', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('participants', models.ManyToManyField(blank=True, related_name='chats', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='post_images')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='post_videos')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('video', models.FileField(upload_to='reels/videos/')),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('content', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('images', models.ManyToManyField(blank=True, related_name='posts_images', to='SnapPulse.image')),
                ('videos', models.ManyToManyField(blank=True, related_name='posts_post_video', to='SnapPulse.video')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('message_type', models.CharField(choices=[('txt', 'Text'), ('img', 'Image'), ('vid', 'Video')], default='txt', max_length=3)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='SnapPulse.chat')),
                ('images', models.ManyToManyField(blank=True, related_name='message_images', to='SnapPulse.image')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
                ('videos', models.ManyToManyField(blank=True, related_name='message_videos', to='SnapPulse.video')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ReadReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_receipts', to='SnapPulse.message')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('message', 'reader')},
            },
        ),
    ]