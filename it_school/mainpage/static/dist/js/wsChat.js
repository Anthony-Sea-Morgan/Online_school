const socket = new WebSocket('ws://127.0.0.1:8000/ws');

socket.onopen = function(e) {
  console.log('WebSocket connection established.');
};

socket.onmessage = function(event) {
  try {
    const message = JSON.parse(event.data);
    const chatMessages = document.getElementById('messages');
    const messageElement = document.createElement('p');
    messageElement.textContent = message.text;
    chatMessages.appendChild(messageElement);
  } catch (e) {
    console.log('Error:', e.message);
  }
};

socket.onclose = function(event) {
  console.log('WebSocket connection closed.');
};

document.getElementById('message-form').onsubmit = function(event) {
  event.preventDefault(); // Предотвращаем отправку формы по умолчанию

  const messageText = document.querySelector('input[name="message_text"]').value;
  const groupId = '{{ group.id }}'; // Получаем идентификатор группы из контекста шаблона

  // Отправляем сообщение через WebSocket
  const socketMessage = {
    type: 'chat_message',
    text: messageText
  };
  socket.send(JSON.stringify(socketMessage));

  // Очищаем поле ввода сообщения
  document.querySelector('input[name="message_text"]').value = '';
};