let currentRoomName = '';

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.room === currentRoomName) {
        const chatLog = document.querySelector(`[data-room-name="${currentRoomName}"] .messages`);
        const messageDiv = document.createElement('div');
        messageDiv.textContent = data.message;
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight;
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};


function sendMessage(username) {
    const messageInput = document.querySelector(`[data-room-name="${currentRoomName}"] .message-text`);
    const message = messageInput.value.trim();

    if (message !== '') {
        chatSocket.send(JSON.stringify({
            'room': currentRoomName,
            'message': message
        }));
        messageInput.value = '';
    }

    return false; // Предотвратить обновление страницы
}
