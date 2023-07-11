import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Класс-потребитель асинхронного WebSocket, отвечающий за обработку соединений и сообщений в чате.
    """
    async def connect(self):
        """
        Метод вызывается, когда клиент подключается к веб-сокету.
        Устанавливает соединение и присоединяет клиента к группе комнаты.
        """
        # Получение имени комнаты из URL-маршрута
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Присоединение к группе комнаты
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Метод вызывается, когда клиент отключается от веб-сокета.

        Отсоединяет клиента от группы комнаты.
        """
        # Покидание группы комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Метод вызывается, когда клиент отправляет сообщение по веб-сокету.
        Получает сообщение от клиента, извлекает информацию об авторе и текущем времени,
        а затем отправляет сообщение всем клиентам в группе комнаты.
        """
        # Получение сообщения от клиента
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author = self.scope['user'].username
        timestamp = datetime.now().strftime('%H:%M')  # Получение текущего времени

        # Отправка сообщения всем в группе комнаты
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': author,
                'timestamp': timestamp
            }
        )

    async def chat_message(self, event):
        """
        Метод вызывается, когда сервер получает сообщение для отправки клиенту.
        Отправляет сообщение указанному клиенту через веб-сокет.
        """
        # Отправка сообщения клиенту
        message = event['message']
        author = event['author']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'timestamp': timestamp
        }))
