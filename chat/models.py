from django.db import models
from users.models import *
from events.models import *

class ChatRoom(models.Model):
    """
    Represents a chat room. Can be linked to an event or used for general/group chats.
    """
    name = models.CharField(max_length=255, blank=True, null=True)  # Optional for group chats
    is_group = models.BooleanField(default=False)  # True for group chats, False for one-on-one
    participants = models.ManyToManyField(CustomUser, related_name='chatrooms')  # Users in the chat room
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='chatrooms', blank=True, null=True)  # Optional link to an event
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.event:
            return f"ChatRoom for Event: {self.event.name}"
        return self.name if self.name else f"ChatRoom {self.id}"


class ChatMessage(models.Model):
    """
    Represents individual messages sent in a chat room.
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')  # Chat room the message belongs to
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')  # User who sent the message
    content = models.TextField()  # Message content
    timestamp = models.DateTimeField(auto_now_add=True)  # When the message was sent

    def __str__(self):
        return f"Message from {self.sender.username} in {self.room}"


class TypingIndicator(models.Model):
    """
    Tracks when a user is typing in a chat room.
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='typing_indicators')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='typing_status')
    is_typing = models.BooleanField(default=False)  # True if the user is typing

    def __str__(self):
        return f"{self.user.username} is typing in {self.room}" if self.is_typing else f"{self.user.username} stopped typing"


class MessageAttachment(models.Model):
    """
    Handles file attachments in messages.
    """
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='chat_attachments/')  # Path to store uploaded files
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.message}"