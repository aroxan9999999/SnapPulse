from django import forms
from .models import Post, Image, Video, Reels


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class VideoForm(forms.ModelForm):
    title = forms.CharField(max_length=255)

    class Meta:
        model = Video
        fields = ['video']


class ReelsForm(forms.ModelForm):
    class Meta:
        model = Reels
        fields = ['title', 'video']
