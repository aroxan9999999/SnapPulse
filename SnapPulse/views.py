from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from ._r_e_d_i_s_ import redis_instance, like_post, dislike_post, get_post_reactions, toggle_heart, increment_counter, \
    toggle_element, get_element_heart_status
from .forms import PostForm, ReelsForm, ImageForm, VideoForm
from .models import Reels, Chat, Image, Video

User = get_user_model()


def home(request):
    reels_form = ReelsForm()
    post_form = PostForm()
    return render(request, 'snappulse/home.html', context=({"reels_form": reels_form, 'post_form': post_form}))


def messages(request):
    users = User.objects.all()
    return render(request, template_name='chat/messages.html', context={"users": users})


def reels(request):
    return render(request, template_name='reels/reels.html')


def chat_room(request, slug):
    return render(request, 'chat/chat_room.html', {
        'room_name': slug
    })


class ReelsListView(ListView):
    model = Reels
    template_name = 'reels/reels.html'
    context_object_name = 'videos'
    ordering = ['-created_at']


class ReelsDetailView(DetailView):
    model = Reels
    template_name = 'reels/reels.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_slug = f"love_reels_{self.object.slug}"
        user_id = self.request.user.id
        chat, created = Chat.objects.get_or_create(title=self.object.title)
        heart_status = get_element_heart_status(video_slug, user_id)
        context['heart_status'] = heart_status
        context['chat'] = chat
        return context


def get_next_video(request):
    current_slug = request.GET.get('current_slug')
    direction = request.GET.get('direction', 'next')  # Получаем направление

    current_video = Reels.objects.get(slug=current_slug)

    if direction == 'next':
        # Получаем следующее видео
        video = Reels.objects.filter(created_at__gt=current_video.created_at).order_by('created_at').first()
    else:
        # Получаем предыдущее видео
        video = Reels.objects.filter(created_at__lt=current_video.created_at).order_by('-created_at').first()

    if video:
        data = {
            'video_slug': video.slug,
            'video_url': video.video.url,
            'heart_status': get_element_heart_status(f'love_reels_{video.slug}', request.user.id),
            'user_id': request.user.id
        }
    else:
        data = {
            'video_slug': None,
            'video_url': None,
        }

    return JsonResponse(data)


def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            # Обработка загруженных файлов
            for file in request.FILES.getlist('file_field'):  # 'file_field' это имя поля в форме
                if file.content_type.startswith('image/'):
                    # Если файл является изображением
                    new_image = Image(image=file)
                    new_image.save()
                    new_post.images.add(new_image)
                elif file.content_type.startswith('video/'):
                    # Если файл является видео
                    new_video = Video(video=file)
                    new_video.save()
                    new_post.videos.add(new_video)

            return redirect(new_post.get_absolute_url())
    else:
        post_form = PostForm()

    return render(request, 'create_post.html', {'post_form': post_form})


def create_reels(request):
    if request.method == 'POST':
        form = ReelsForm(request.POST, request.FILES)
        if form.is_valid():
            new_reel = form.save(commit=False)
            new_reel.user = request.user
            new_reel.save()
            return redirect(new_reel.get_absolute_url())
    else:
        form = ReelsForm()

    return render(request, 'create_reels.html', {'form': form})


@login_required
@require_POST
def like_post_view(request, post_id):
    user_id = request.user.id
    like_post(redis_instance, user_id, post_id)
    post_reactions = get_post_reactions(redis_instance, post_id)
    return JsonResponse(post_reactions)


@login_required
@require_POST
def dislike_post_view(request, post_id):
    user_id = request.user.id
    dislike_post(redis_instance, user_id, post_id)
    post_reactions = get_post_reactions(redis_instance, post_id)
    return JsonResponse(post_reactions)


@login_required
@require_POST
def heart_post(request, post_id):
    user_id = request.user.id
    hearted = toggle_heart(redis_instance, user_id, post_id)
    return JsonResponse({'hearted': hearted})


@login_required
@require_POST
def get_reels_view(request, key):
    response = increment_counter(key)
    return JsonResponse(response)


@login_required
@require_POST
def love(request, key, value, return_all=False):
    # return_all = request.GET.get('return_all', 'false').lower() == 'true'
    response = toggle_element(key, value, return_all)
    return JsonResponse(response)
