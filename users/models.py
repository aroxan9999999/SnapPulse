from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import format_html


class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics/', verbose_name="Avatar")
    bio = models.TextField(blank=True, verbose_name="Biography")
    following = models.ManyToManyField(
        'self',
        through='UserRelation',
        related_name='followers',
        symmetrical=False,
        verbose_name="Following"
    )
    email = models.EmailField(unique=True)
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True)

    def get_profile_pic(self):
        if self.profile_pic:
            return format_html('<img src="{}" width="50" height="50" />', self.profile_pic.url)
        return "-"

    get_profile_pic.short_description = 'Profile Picture'


class UserRelation(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followed_by")
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="follows")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Followed Since")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow')
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


