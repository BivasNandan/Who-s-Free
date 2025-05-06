import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Verify that the user is a participant in the chat room
        try:
            self.chat_room = await database_sync_to_async(ChatRoom.objects.get)(id=self.room_name)
            is_participant = await database_sync_to_async(self.chat_room.participants.filter(id=self.scope['user'].id).exists)()
            if not is_participant:
                await self.close()
                return
        except ChatRoom.DoesNotExist:
            await self.close()
            return

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']

        # Save the message to the database
        await database_sync_to_async(ChatMessage.objects.create)(
            room=self.chat_room,
            sender=sender,
            content=message
        )

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # This must match the method name below
                'message': message,
                'sender': sender.username,
            }
        )

    async def chat_message(self, event):
        """
        Handles the 'chat_message' event and sends the message to the WebSocket.
        """
        message = event['message']
        sender = event['sender']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))