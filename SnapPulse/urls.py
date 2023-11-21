from django.urls import path
from . import views

urlpatterns = [
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('heart_post/<int:post_id>/', views.heart_post, name='heart_post'),
    path('', views.home, name='home'),
    path('chat/<slug:slug>/', views.chat_room, name='chat_room'),
    path('messages/', views.messages, name='messages'),
    path('reels/', views.ReelsListView.as_view(), name='reels'),
    path('reels/<slug:slug>/', views.ReelsDetailView.as_view(), name='reels_detail'),
    path('get_next_video/', views.get_next_video, name='get_next_video'),
    path('get_reels_view/<str:key>/', views.get_reels_view, name='reels_view_count'),
    path('love/<str:key>/<int:value>/', views.love, name='love'),
    path('reels/create/', views.create_reels, name='create_reels'),
]
