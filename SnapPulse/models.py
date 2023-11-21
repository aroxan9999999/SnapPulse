from django.db import models
from django.urls import reverse

from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.utils.safestring import SafeString


class Image(models.Model):
    image = models.ImageField(upload_to='post_images')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, db_index=True)

    def __str__(self):
        return f"Image: {self.image.name}"

    def image_tag(self) -> SafeString:
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')

    image_tag.short_description = 'Image Preview'


class Video(models.Model):
    video = models.FileField(upload_to='post_videos')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, db_index=True)

    def __str__(self):
        return f"Video: {self.video.name}"

    def video_tag(self) -> SafeString:
        return mark_safe(
            f'<video width="150" height="150" controls><source src="{self.video.url}" type="video/mp4">Your browser does not support the video tag.</video>')

    video_tag.short_description = 'Video Preview'


class Comments(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ('-created_at',)


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, db_index=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    images = models.ManyToManyField(Image, blank=True, related_name='posts_images')
    videos = models.ManyToManyField(Video, blank=True, related_name='posts_post_video')
    messages = models.ManyToManyField('Message')

    def __str__(self):
        return f"Post by {self.author.name}"

    class Meta:
        ordering = ['-created_at']


class Chat(models.Model):
    title = models.CharField(max_length=255, unique=True, null=True, blank=True, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, db_index=True)
    direct = models.BooleanField(default=False)
    participants = models.ManyToManyField(CustomUser, related_name='chats', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title if self.title else f"Chat {self.pk}"

    class Meta:
        ordering = ['title']


class Message(models.Model):
    class MessageType(models.TextChoices):
        TEXT = 'txt', _('Text')
        IMAGE = 'img', _('Image')
        VIDEO = 'vid', _('Video')

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(blank=True, null=True)
    images = models.ManyToManyField(Image, blank=True, related_name='message_images')
    videos = models.ManyToManyField(Video, blank=True, related_name='message_videos')
    message_type = models.CharField(max_length=3, choices=MessageType.choices, default=MessageType.TEXT)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message_type} Message {self.id} by {self.sender.name}"

    class Meta:
        ordering = ['-timestamp']


class ReadReceipt(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='read_receipts')
    reader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='read_messages')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'reader')

    def __str__(self):
        return f"Message {self.message.id} read by {self.reader.username} at {self.read_at}"


class Reels(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.FileField(upload_to='reels/videos/')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    messages = models.ManyToManyField('Message')

    def get_absolute_url(self):
        return reverse('reels_detail', args=[str(self.slug)])

