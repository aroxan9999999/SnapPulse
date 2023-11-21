let lastScrollTop = 0;
let isProcessing = false; // Для контроля частоты вызовов функции

document.addEventListener('scroll', function() {
    if (isProcessing) return;
    isProcessing = true;
    setTimeout(() => { isProcessing = false; }, 1000); // Ограничиваем вызов функции

    var st = window.pageYOffset || document.documentElement.scrollTop;
    if (st > lastScrollTop) {
        loadVideo('next');
    } else {
        loadVideo('previous');
    }
    lastScrollTop = st <= 0 ? 0 : st;
}, false);

function loadVideo(direction) {
    var currentVideo = document.getElementById('currentVideo');
    var currentSlug = currentVideo.parentElement.id;

    fetch(`/get_next_video/?current_slug=${currentSlug}&direction=${direction}`)
        .then(response => response.json())
        .then(data => {
            if (data.video_url) {
                console.log(data)
                updateVideoContainer(data.video_url, data.video_slug, data.heart_status, data.user_id);
            }
        })
        .catch(error => console.error('Error:', error));
}

function updateVideoContainer(videoUrl, videoSlug, heartStatus, userId) {
    console.log(videoUrl, videoSlug, heartStatus, userId)
    var videoContainer = document.getElementById('videoContainer');
    var heartImageUrl = heartStatus.status === 'added' ? '/static/icons/love_heart.png' : '/static/icons/easy_heart.png';

    videoContainer.innerHTML = `
        <div id="${videoSlug}" class="reels">
            <video id="currentVideo" autoplay loop>
                <source src="${videoUrl}" type="video/mp4">
            </video>
        </div>
        </div>
            <div id="video_${videoSlug}" class="block_icons">
            <div class="icons heart" style="background-image: url('${heartImageUrl}');" onclick="toggleLove('love_reels_${videoSlug}', ${userId})"><span class="count">${heartStatus.count}</span></div>
            <div class="icons  chat" onclick="toggleChatDisplay()"></div>
            <div class="icons  view">
                <span class="view_count"></span>
            </div>
            <div class="chat_content{{video.video.pk}}"></div>
        </div>
        <div id='chat_content_reels_{{chat.slug}}' class="reels_chat"></div>
            <div class="chat_form">
                <input id="chat-message-input" type="text" size="100"><br>
                <input id="chat-message-submit" type="button" value="Send">
            </div>
            <div class="message">
                <p class="author"><span class="author_name"></span></p><br>
                <p class="author_text"></p>
            </div>
        </div>
    `;
    let video_slug = `view_${videoSlug}`;
    incrementViewCount(video_slug);
    var currentPath = window.location.pathname;
    var endIndex = currentPath.indexOf("/reels/");
    var location = currentPath.substring(0, endIndex + 6)
    var newUrl = `${location}/${videoSlug}`;
    history.pushState({ path: newUrl }, '', newUrl);
    const videoElement = document.getElementById('currentVideo');
    videoElement.addEventListener('click', function() {
        if (this.muted) {
            this.muted = false;
        } else {
            this.muted = true;
        }
    });

    videoElement.addEventListener('dblclick', function() {
        if (this.requestFullscreen) {
            this.requestFullscreen();
        } else if (this.mozRequestFullScreen) { /* Firefox */
            this.mozRequestFullScreen();
        } else if (this.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
            this.webkitRequestFullscreen();
        } else if (this.msRequestFullscreen) { /* IE/Edge */
            this.msRequestFullscreen();
        }
    });
}
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

function toggleChatDisplay() {
    var chatContent = document.getElementsByClassName('reels_chat');
    for (var i = 0; i < chatContent.length; i++) {
        if (chatContent[i].style.display === 'none' || chatContent[i].style.display === '') {
            chatContent[i].style.display = 'flex';
        } else {
            chatContent[i].style.display = 'none';
        }
    }
}

function toggleLove(key, userId) {
    fetch(`/love/${key}/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        const heartIcon = document.querySelector('.heart');

        if (heartIcon) {
            const countSpan = heartIcon.querySelector('.count');
            countSpan.textContent = data.count;

           if (data.status === 'added') {
            heartIcon.style.backgroundImage = "url('/media/icons/love_heart.png')";
        } else {
             heartIcon.style.backgroundImage = "url('/media/icons/easy_heart.png')";
        }

        } else {
            console.error('Heart icon not found');
        }
    })
    .catch(error => console.error('Error:', error));
}


function incrementViewCount(videoSlug) {
    fetch(`/get_reels_view/view_${videoSlug}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.querySelectorAll('.view_count').forEach(viewCountSpan => {
            viewCountSpan.textContent = data.count;
        });
    })
    .catch(error => console.error('Error:', error));
}


