import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Присоединение к группе комнаты
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Покидание группы комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
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
        # Отправка сообщения клиенту
        message = event['message']
        author = event['author']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'timestamp': timestamp
        }))
