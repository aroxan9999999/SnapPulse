document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.upload-form').forEach(form => {
    const fileInput = form.querySelector('.file-input');
    const fileCountSpan = form.querySelector('.file-count');
    const previewContainer = form.querySelector('.file-preview-container');


        fileInput.addEventListener('change', function() {
            updateFilePreview();
            updateFileCount();
        });

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log('Форма отправлена для пользователя с ID ' + form.dataset.chatId);
            fileInput.value = '';
            form.querySelector('.message-text').value = '';
            updateFileCount();
            previewContainer.innerHTML = '';
        });

        function updateFileCount() {
            const fileCount = fileInput.files.length;
            fileCountSpan.textContent = fileCount > 0 ? `${fileCount} файлов` : '+';
        }

        function updateFilePreview() {
            previewContainer.innerHTML = '';
            Array.from(fileInput.files).forEach((file, index) => {
                const fileReader = new FileReader();
                const previewElement = document.createElement('div');
                previewElement.classList.add('file-preview');

                const removeButton = document.createElement('span');
                removeButton.textContent = '✖';
                removeButton.classList.add('remove-file');
                removeButton.addEventListener('click', function() {
                    updateFileList(index);
                });
                previewElement.appendChild(removeButton);

                if (file.type.startsWith('image/')) {
                    fileReader.onload = function(e) {
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        previewElement.appendChild(img);
                    };
                    fileReader.readAsDataURL(file);
                } else if (file.type.startsWith('video/')) {
                    const video = document.createElement('video');
                    video.controls = true;
                    video.autoplay = true;
                    video.muted = true;
                    video.loop = true;
                    video.src = URL.createObjectURL(file);
                    previewElement.appendChild(video);
                }

                previewContainer.appendChild(previewElement);
            });
            updatePreviewSizes();
        }

        function updatePreviewSizes() {
            const previews = previewContainer.querySelectorAll('.file-preview');
            const singleWidth = '100px';
            const defaultWidth = '100px';

            if (previews.length === 1) {
                previews[0].style.width = singleWidth;
            } else {
                previews.forEach(preview => {
                    preview.style.width = defaultWidth;
                });
            }
        }

        function updateFileList(indexToRemove) {
            const newFileList = Array.from(fileInput.files).filter((_, index) => index !== indexToRemove);
            const dataTransfer = new DataTransfer();
            newFileList.forEach(file => dataTransfer.items.add(file));
            fileInput.files = dataTransfer.files;
            updateFilePreview();
            updateFileCount();
        }
    });
});
