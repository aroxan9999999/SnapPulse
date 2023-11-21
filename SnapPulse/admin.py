from django.contrib import admin
from .models import Chat, Message, Post, Video, Reels
from django.utils.html import format_html
from .models import Image


class ChatAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'direct', 'created_at')
    search_fields = ('title', 'participants__username')
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


class VideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'slug')
    prepopulated_fields = {'slug': ('video',)}


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'slug')
    readonly_fields = ('image_tag',)
    prepopulated_fields = {'slug': ('image',)}

    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width="150" height="150" style="border-radius:50%; border:3px solid #FF69B4;/>',
            obj.image.url)

    image_tag.short_description = 'Image Preview'


class ReelsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'slug', 'display_video')
    fields = ('title', 'user', 'video', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    def display_video(self, obj):
        if obj.video:
            video_url = obj.video.url
            return format_html(
                '<video width="120" height="140" border-radius="50" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>',
                video_url)
        else:
            return "No video"

    display_video.short_description = 'Video Preview'


admin.site.register(Reels, ReelsAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message)
admin.site.register(Post, PostAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Image, ImageAdmin)
