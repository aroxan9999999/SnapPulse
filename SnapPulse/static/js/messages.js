function toggleChat(username) {
    // Переключение активного пользователя
    document.querySelectorAll('.user').forEach(user => {
        user.classList.remove('active');
    });
    document.querySelector('.user[onclick="toggleChat(\'' + username + '\')"]').classList.add('active');

    // Показать соответствующий чат
    document.querySelectorAll('.chat').forEach(chat => {
        chat.style.display = 'none';
    });
    document.getElementById('chat_' + username).style.display = 'block';
}

function sendMessage(username) {
    const messageInput = document.querySelector(`#chat_${username} input[name='message']`);
    const message = messageInput.value;

    if (message.trim() !== '') {
        // Здесь код для отправки сообщения на сервер

        // Добавление сообщения в чат
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', 'mine');
        messageDiv.textContent = message;
        document.querySelector(`#chat_${username} .messages`).appendChild(messageDiv);

        // Очистить поле ввода
        messageInput.value = '';
    }
    return false; // Предотвратить обновление страницы
}


