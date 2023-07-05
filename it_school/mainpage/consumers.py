from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CustomConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, event):
        group_id = self.scope['url_route']['kwargs']['group_id']
        group_name = f'chat_{group_id}'
        await self.channel_layer.group_add(group_name, self.channel_name)
        await self.accept()

    async def websocket_receive(self, event):
        message = event['text']
        group_id = self.scope['url_route']['kwargs']['group_id']
        group_name = f'chat_{group_id}'
        await self.channel_layer.group_send(group_name, {'type': 'chat_message', 'text': message})

    async def websocket_disconnect(self, event):
        group_id = self.scope['url_route']['kwargs']['group_id']
        group_name = f'chat_{group_id}'
        await self.channel_layer.group_discard(group_name, self.channel_name)

    async def chat_message(self, event):
        message = event['text']
        await self.send(text_data=json.dumps({'text': message}))