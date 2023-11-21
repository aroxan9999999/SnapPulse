function send_message(to) {
    document.getElementById('message-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append('content', document.getElementById('message-input').value);
    const fileInput = document.getElementById('message-file');
    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);
    }

    fetch('/send_message', {
        method: 'POST',
        body: formData  // Теперь отправляем FormData
    })
    .then(response => response.json())
    .then(data => {
        // Обработка ответа
        console.log(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

}

document.querySelectorAll('.carousel-control').forEach(button => {
    button.addEventListener('click', function() {
        const offset = this.classList.contains('right') ? 1 : -1;
        const slides = this.closest('.post-content').querySelector('.carousel').children;
        const activeSlide = this.closest('.post-content').querySelector('.carousel-item.active');
        let newIndex = [...slides].indexOf(activeSlide) + offset;

        if (newIndex < 0) newIndex = slides.length - 1;
        if (newIndex >= slides.length) newIndex = 0;

        slides[newIndex].classList.add('active');
        activeSlide.classList.remove('active');
    });
});


// Получаем элементы
var modal = document.getElementById("createPostModal");
var trigger = document.getElementById("createPostTrigger");
var close = document.querySelector(".close");

trigger.onclick = function() {
    modal.style.display = "block";
}


close.onclick = function() {
    modal.style.display = "none";
}


window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


document.getElementById("createPostForm").onsubmit = function(event) {
    event.preventDefault();
}
